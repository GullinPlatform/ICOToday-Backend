import random
from datetime import timedelta

from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import check_password
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from rest_framework_jwt.settings import api_settings
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny

from .models import Account, VerifyToken, AccountVerifyInfo, Team
from .serializers import AccountSerializer, TeamSerializer, BasicTeamSerializer


def send_verify_token(email=None, phone=None):
	if email:
		token_instance, created = VerifyToken.objects.get_or_create(email=email)

		# if token exists, recreate one
		if created:
			token_instance.expire_time = timezone.now() + timedelta(hours=5)
			token_instance.token = random.randint(0, 10 ** 6 - 1)
			token_instance.save()
		token = token_instance.token
	# email = EmailMessage(subject, render_to_string('email/%s.html' % template, ctx), 'no-reply@icotoday.io', [to])
	# email.content_subtype = 'html'
	# email.send()
	if phone:
		token_instance, created = VerifyToken.objects.get_or_create(phone=phone)

		# if token exists, recreate one
		if created:
			token_instance.expire_time = timezone.now() + timedelta(hours=5)
			token_instance.token = random.randint(0, 10 ** 6 - 1)
			token_instance.save()

		token = token_instance.token


class AccountRegisterViewSet(viewsets.ViewSet):
	parser_classes = (MultiPartParser, FormParser, JSONParser)
	permission_classes = (AllowAny,)

	def register(self, request):
		serializer = AccountSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.save()
		if not user:
			return Response({'error': 'Must provide Phone or Email.'}, status=status.HTTP_400_BAD_REQUEST)
		jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
		jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
		payload = jwt_payload_handler(user)
		token = jwt_encode_handler(payload)

		return Response({'token': token}, status=status.HTTP_201_CREATED)

	def send_token(self, request):
		if request.data['email']:
			send_verify_token(email=request.data['email'])
		if request.data['phone']:
			send_verify_token(phone=request.data['phone'])
		return Response(status=status.HTTP_200_OK)

	def verify_token(self, request):
		if not request.data['token']:
			return Response(status=status.HTTP_400_BAD_REQUEST)

		token_instance = get_object_or_404(VerifyToken.objects.all(), token=request.data['token'])
		# check is_expired
		if token_instance.is_expired:
			return Response({'message': 'Token is expired'}, status=status.HTTP_400_BAD_REQUEST)

		token_instance.account.is_verified = True
		token_instance.is_expired = True
		return Response(status=status.HTTP_200_OK)

	def forget_password(self, request, token=None):
		token_queryset = VerifyToken.objects.all()
		# verify token
		if request.method == 'POST':
			# if token not exist return 404 here
			token_instance = get_object_or_404(token_queryset, token=token)
			# check is_expired
			if token_instance.is_expired:
				return Response(status=status.HTTP_404_NOT_FOUND)
			# else return 200
			return Response(status=status.HTTP_200_OK)

		# change password
		elif request.method == 'PUT':
			# if token not exist return 404 here
			token_instance = get_object_or_404(token_queryset, token=token)
			# check is_expired
			if token_instance.is_expired:
				return Response(status=status.HTTP_404_NOT_FOUND)
			# set new password to user
			token_instance.account.set_password(request.data['password'])
			token_instance.account.save()
			token_instance.is_expired = True
			return Response(status=status.HTTP_200_OK)


class AccountViewSet(viewsets.ViewSet):
	queryset = Account.objects.exclude(is_staff=1)
	parser_classes = (MultiPartParser, FormParser, JSONParser)
	permission_classes = (IsAuthenticatedOrReadOnly,)

	def retrieve(self, request, pk):
		user = get_object_or_404(self.queryset, pk=pk)
		serializer = AccountSerializer(user)
		return Response(serializer.data)

	def destroy(self, request, pk=None):
		if request.user.is_admin or request.user.pk == int(pk):
			user = get_object_or_404(self.queryset, pk=pk)
			user.delete()
			return Response(status=status.HTTP_200_OK)
		else:
			return Response(status=status.HTTP_403_FORBIDDEN)

	@staticmethod
	def me(request):
		if request.method == 'GET':
			serializer = AccountSerializer(request.user)
			return Response(serializer.data)

	@staticmethod
	def change_password(request):
		# If password or old-password not in request body
		if not request.data['old-password'] or request.data['password']:
			# Return error message with status code 400
			return Response(status=status.HTTP_400_BAD_REQUEST)
		try:
			#  if old-password match
			if check_password(request.data['old-password'], request.user.password):
				# change user password
				request.user.set_password(request.data['password'])
				request.user.save()
				return Response(status=status.HTTP_200_OK)
			else:
				# else return with error message and status code 400
				return Response({'ERROR': 'Password not match'}, status=status.HTTP_400_BAD_REQUEST)
		except:
			# If exception return with status 400
			return Response(status=status.HTTP_400_BAD_REQUEST)

	def verify_info(self, request):
		if request.user.is_company:
			info = AccountVerifyInfo(account=request.user,
			                         company_name=request.data['company_name'],
			                         company_register_file=request.data['company_register_file'],
			                         company_phone=request.data['company_phone'],
			                         company_contact=request.data['company_contact'],
			                         company_email=request.data['company_email'],
			                         company_address=request.data['company_address'],
			                         company_field=request.data['company_field'],
			                         )
		else:
			info = AccountVerifyInfo(account=request.user,
			                         real_name=request.data['real_name'],
			                         working_at=request.data['working_at'],
			                         legal_id=request.data['legal_id'],
			                         legal_id_type=request.data['legal_id_type'],
			                         wechat=request.data['wechat'],
			                         qq=request.data['qq'],
			                         phone=request.data['phone'],
			                         )
			if request.data['birthday']:
				info.birthday = request.data['birthday']

		info.save()
		request.user.is_verified = 1
		request.user.save()
		return Response(status=status.HTTP_201_CREATED)

	# @api_view(['GET', 'POST', 'OPTION'])
	# @permission_classes((IsAuthenticated,))
	# @parser_classes((MultiPartParser, FormParser,))
	# def account_avatar(request):
	# 	if request.method == 'POST':
	# 		from StringIO import StringIO
	# 		from django.core.files.uploadedfile import InMemoryUploadedFile
	# 		from resizeimage import resizeimage
	# 		from PIL import Image
	# 		upload = request.FILES.get('file', False)
	# 		if not upload:
	# 			return Response(status=status.HTTP_400_BAD_REQUEST)
	# 		filename, file_extension = upload.name.split('.')
	# 		with Image.open(upload) as image:
	# 			image2x = resizeimage.resize_cover(image, [128, 128])
	# 			image1x = resizeimage.resize_cover(image, [48, 48])
	# 			img2x_name = str(request.user.id) + '.2x' + file_extension
	# 			img1x_name = str(request.user.id) + '.1x' + file_extension
	# 			img2x_io = StringIO()
	# 			img1x_io = StringIO()
	# 			image2x.save(img2x_io, image.format)
	# 			image1x.save(img1x_io, image.format)
	# 			image2x_file = InMemoryUploadedFile(img2x_io, None, img2x_name, 'image/' + image.format,
	# 			                                    img2x_io.len, None)
	# 			image1x_file = InMemoryUploadedFile(img1x_io, None, img1x_name, 'image/' + image.format,
	# 			                                    img1x_io.len, None)
	#
	# 		new_avatar = Avatar.objects.create(avatar2x=image2x_file, avatar1x=image1x_file)
	# 		request.user.avatar = new_avatar
	# 		request.user.save()
	# 		return Response({'data': 'success'}, status=status.HTTP_200_OK)
	# 	elif request.method == 'GET':
	# 		serializer = AvatarSerializer(request.user.avatar)
	# 		return Response(serializer.data)


class TeamViewSet(viewsets.ViewSet):
	queryset = Team.objects.all()
	parser_classes = (MultiPartParser, FormParser, JSONParser)
	permission_classes = (IsAuthenticatedOrReadOnly,)

	def list(self, request):
		serializer = BasicTeamSerializer(self.queryset, many=True)
		return Response(serializer.data)

	def retrieve(self, request, pk=None):
		team = get_object_or_404(self.queryset, pk=pk)
		serializer = TeamSerializer(team)
		return Response(serializer.data)

	def create(self, request):
		if request.data.get('name') and request.data.get('description'):
			team = Team.objects.create(
				name=request.data.get('name'),
				description=request.data.get('description')
			)
			request.user.team = team
			request.use.save()
			return Response(status=status.HTTP_201_CREATED)
		else:
			return Response(status=status.HTTP_400_BAD_REQUEST)
