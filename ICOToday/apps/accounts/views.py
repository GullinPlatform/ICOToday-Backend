import random
import string

from datetime import timedelta, datetime

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

from .models import Account, VerifyToken, Team, AccountInfo
from .serializers import AuthAccountSerializer, TeamSerializer, BasicTeamSerializer, BasicAccountSerializer, AccountInfoSerializer

from ..posts.models import Post
from ..posts.serializers import PostSerializer


def send_email(receiver_list, subject, template_name, ctx):
	email = EmailMessage(subject, render_to_string('email/%s.html' % template_name, ctx), 'no-reply@icotoday.io', receiver_list)
	email.content_subtype = 'html'
	email.send()


def get_user_verify_token(user=None, email=None):
	if user:
		token_instance, created = VerifyToken.objects.get_or_create(user_id=user.id)
	elif email:
		user = get_object_or_404(Account.objects.all(), email=email)
		token_instance, created = VerifyToken.objects.get_or_create(user_id=user.id)
	else:
		return None

	if created or not token_instance.is_expired:
		return token_instance
	else:
		token_instance.expire_time = timezone.now() + timedelta(hours=5)
		token_instance.token = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(32)])
		token_instance.save()
		return token_instance


class AccountRegisterViewSet(viewsets.ViewSet):
	parser_classes = (MultiPartParser, FormParser, JSONParser)
	permission_classes = (AllowAny,)

	def register(self, request):
		serializer = AuthAccountSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.save()

		# If ICO Company, have team name
		if request.data.get('type') is 0:
			user.info.first_name = request.data.get('first_name')
			user.info.last_name = request.data.get('last_name')
			team = Team.objects.create(name=request.data.get('team_name'))
			user.info.team_id = team.id
			user.info.save()

		# return token right away
		jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
		jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
		payload = jwt_payload_handler(user)
		token = jwt_encode_handler(payload)

		user_verify_token = get_user_verify_token(user)

		send_email(receiver_list=[user.email],
		           subject='ICOToday - Email Verification',
		           template_name='EmailVerification',
		           ctx={'user': user, 'token': user_verify_token}
		           )

		return Response({'token': token}, status=status.HTTP_201_CREATED)

	def invited_register(self, request):
		if request.data.get('email'):
			# TODO: Not sure
			serializer = AuthAccountSerializer(data=request.data, partial=True)
			serializer.is_valid(raise_exception=True)
			user = serializer.save()

			# return token right away
			jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
			jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
			payload = jwt_payload_handler(user)
			token = jwt_encode_handler(payload)

			return Response({'token': token}, status=status.HTTP_400_BAD_REQUEST)
		else:
			return Response(status=status.HTTP_400_BAD_REQUEST)

	def email_verify(self, request, token=None):
		# Verify Token
		if request.method == 'GET':
			if not token:
				return Response(status=status.HTTP_400_BAD_REQUEST)

			token_instance = get_object_or_404(VerifyToken.objects.all(), token=token)
			# check is_expired
			if token_instance.is_expired:
				return Response({'message': 'Token is expired'}, status=status.HTTP_400_BAD_REQUEST)

			token_instance.account.is_verified = True
			token_instance.expire_time = datetime.utcnow()
			return Response(status=status.HTTP_200_OK)
		# Resend Email
		elif request.method == 'POST':
			user_verify_token = get_user_verify_token(request.user)

			send_email(receiver_list=[request.user.email],
			           subject='ICOToday - Email Verification',
			           template_name='EmailVerification',
			           ctx={'user': request.user, 'token': user_verify_token}
			           )

	def forget_password(self, request, token=None):
		token_queryset = VerifyToken.objects.all()
		# verify token
		if request.method == 'GET':
			# if token not exist return 404 here
			token_instance = get_object_or_404(token_queryset, token=token)
			# check is_expired
			if token_instance.is_expired:
				return Response(status=status.HTTP_404_NOT_FOUND)
			# else return 200
			return Response(status=status.HTTP_200_OK)

		# get token
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
			token_instance.expire_time = datetime.utcnow()
			return Response(status=status.HTTP_200_OK)


class AccountViewSet(viewsets.ViewSet):
	queryset = Account.objects.exclude(is_staff=1)
	parser_classes = (MultiPartParser, FormParser, JSONParser)
	permission_classes = (IsAuthenticatedOrReadOnly,)

	def retrieve(self, request, pk):
		user = get_object_or_404(self.queryset, pk=pk)
		serializer = BasicAccountSerializer(user)
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
			serializer = BasicAccountSerializer(request.user)
			return Response(serializer.data)
		elif request.method == 'PUT':
			if request.data.get('avatar'):
				request.user.info.avatar = request.data.get('avatar')
				request.user.info.save()
				return Response(status=status.HTTP_200_OK)
			else:
				serializer = AccountInfoSerializer(request.user.info, data=request.data, partial=True)
				serializer.is_valid(raise_exception=True)
				serializer.save()
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

	def marked_posts(self, request, pk=None):
		if pk:
			account = get_object_or_404(self.queryset, pk=pk)
			serializer = PostSerializer(account.marked_posts.all(), many=True)
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			serializer = PostSerializer(request.user.marked_posts.all(), many=True)
			return Response(serializer.data, status=status.HTTP_200_OK)

	def created_posts(self, request, pk=None):
		if pk:
			account = get_object_or_404(self.queryset, pk=pk)
			if account.info.team:
				serializer = PostSerializer(Post.objects.filter(team_id=account.info.team.id), many=True)
				return Response(serializer.data, status=status.HTTP_200_OK)
			else:
				return Response([], status=status.HTTP_200_OK)

		else:
			serializer = PostSerializer(Post.objects.filter(team_id=request.user.info.team.id), many=True)
			return Response(serializer.data, status=status.HTTP_200_OK)


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

	def update(self, request, pk):
		team = get_object_or_404(self.queryset, pk=pk)

		if request.data.get('name'):
			team.name = request.data.get('name')

		if request.data.get('description'):
			team.description = request.data.get('description')

		team.save()
		return Response(status=status.HTTP_200_OK)

	def add_team_member(self, request, pk):
		# IMPORTANT: Here pk is Team Pk!
		if request.method == 'PATCH':
			team = get_object_or_404(self.queryset, pk=pk)
			if request.data.get('email'):
				# Must use == not is here, otherwise type dismatch
				is_advisor = True if request.data.get('is_advisor') == 'true' else False
				print request.data.get('avatar')
				info = AccountInfo.objects.create(
					avatar=request.data.get('avatar'),
					first_name=request.data.get('first_name'),
					last_name=request.data.get('last_name'),
					title=request.data.get('title'),
					description=request.data.get('description'),
					team_id=pk,
					is_advisor=is_advisor,
					linkedin=request.data.get('linkedin', ''),
					twitter=request.data.get('twitter', ''),
					slack=request.data.get('slack', ''),
					telegram=request.data.get('telegram', ''),
				)
				team.members.add(info)

				user = Account.objects.create_user(
					email=request.data.get('email'),
					info=info,
					type=1,  # ICO Company
					password=''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(32)])
				)

				user_verify_token = get_user_verify_token(user)
				send_email(receiver_list=[user.email],
				           subject='ICOToday - Your Team is Waiting You',
				           template_name='TeamInvitation',
				           ctx={'user': user, 'token': user_verify_token}
				           )

				return Response(status=status.HTTP_200_OK)
			else:
				return Response(status=status.HTTP_400_BAD_REQUEST)
		# IMPORTANT: Here pk is Account Pk!
		elif request.method == 'DELETE':
			info = get_object_or_404(AccountInfo.objects.all(), pk=pk)
			info.team.members.remove(info)
			return Response(status=status.HTTP_200_OK)
