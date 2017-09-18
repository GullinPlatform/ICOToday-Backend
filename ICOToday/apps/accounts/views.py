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
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated

from .models import Account, VerifyToken, Team, AccountInfo, ExpertApplication
from .serializers import AuthAccountSerializer, TeamSerializer, BasicTeamSerializer, BasicAccountSerializer, AccountInfoSerializer, ExpertApplicationSerializer

from ..posts.models import Post
from ..posts.serializers import PostSerializer


def send_email(receiver_list, subject, template_name, ctx):
	email = EmailMessage(subject, render_to_string('email/%s.html' % template_name, ctx), 'no-reply@icotoday.io', receiver_list)
	email.content_subtype = 'html'
	email.send()


def get_user_verify_token(user=None, email=None, only_digit=False):
	if user:
		token_instance, created = VerifyToken.objects.get_or_create(account_id=user.id)
	elif email:
		user = get_object_or_404(Account.objects.all(), email=email)
		token_instance, created = VerifyToken.objects.get_or_create(account_id=user.id)
	else:
		return None

	token_instance.expire_time = timezone.now() + timedelta(hours=24)
	if only_digit:
		token_instance.token = ''.join([random.choice(string.digits) for n in xrange(6)])
	else:
		token_instance.token = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(16)])
	token_instance.save()
	return token_instance


def verify_token(token=None, user=None):
	if token and user:
		token_instance = VerifyToken.objects.get(token=token, account_id=user.id)
	elif token and not user:
		token_instance = VerifyToken.objects.get(token=token)
	else:
		return False

	if not token_instance:
		return False

	elif token_instance.is_expired:
		return False

	else:
		token_instance.expire_time = timezone.now() - timedelta(days=10)
		token_instance.token = ''
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
		           ctx={'user': user, 'token': user_verify_token.token})

		return Response({'token': token}, status=status.HTTP_201_CREATED)

	def invited_register(self, request, token):
		# Get user register need info
		if request.method == 'GET':
			token_instance = get_object_or_404(VerifyToken.objects.all(), token=token)
			if token_instance.is_expired:
				return Response({'detail': 'Token Expired'}, status=status.HTTP_400_BAD_REQUEST)
			serializer = BasicAccountSerializer(token_instance.account)
			return Response(serializer.data, status=status.HTTP_200_OK)

		# Invited user change password
		elif request.method == 'POST':
			if request.data.get('password'):
				token_instance = verify_token(token=token)
				if token_instance:
					token_instance.account.set_password(request.data.get('password'))
					token_instance.account.is_verified = True
					token_instance.account.save()

					# return auth token right away
					jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
					jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
					payload = jwt_payload_handler(token_instance.account)
					token = jwt_encode_handler(payload)

					return Response({'token': token}, status=status.HTTP_201_CREATED)
				else:
					return Response({'detail': 'Token Invalid'}, status=status.HTTP_400_BAD_REQUEST)
			else:
				return Response({'detail': 'No password provided'}, status=status.HTTP_400_BAD_REQUEST)

	def email_verify(self, request, token=None):
		# Verify Token
		if request.method == 'GET':
			if not token:
				return Response(status=status.HTTP_400_BAD_REQUEST)

			token_instance = verify_token(token=token)
			# check is_expired
			if not token_instance:
				return Response({'message': 'Token is expired'}, status=status.HTTP_400_BAD_REQUEST)

			token_instance.account.is_verified = True
			token_instance.account.save()

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
				return Response({'detail': 'Token Expired'}, status=status.HTTP_400_BAD_REQUEST)
			# else return 200
			return Response(status=status.HTTP_200_OK)

		# send email
		if request.method == 'POST':
			if request.data.get('email'):
				token_instance = get_user_verify_token(email=request.data.get('email'))
				send_email(receiver_list=[request.data.get('email')],
				           subject='ICOToday - Password Reset',
				           template_name='PasswordReset',
				           ctx={'token': token_instance.token}
				           )
				return Response(status=status.HTTP_200_OK)

			else:
				return Response(status=status.HTTP_400_BAD_REQUEST)

		# change password
		elif request.method == 'PUT':
			# if token not exist return 404 here
			token_instance = verify_token(token=token)
			# check is_expired
			if not token_instance:
				return Response(status=status.HTTP_400_BAD_REQUEST)
			# set new password to user
			token_instance.account.set_password(request.data['password'])
			token_instance.account.save()
			token_instance.expire_time = timezone.now() - timedelta(hours=24)
			token_instance.save()
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

	def two_factor_auth(self, request):
		# Send Email
		if request.method == 'POST':
			token_instance = get_user_verify_token(user=request.user, only_digit=True)
			send_email(receiver_list=[request.user.email],
			           subject='ICOToday - Verification Token',
			           template_name='TwoFactorAuth',
			           ctx={'token': token_instance.token})
			return Response(status=status.HTTP_200_OK)

		# Verify Token
		elif request.method == 'PUT':
			token_instance = verify_token(token=request.data.get('token'), user=request.user)

			if token_instance:
				return Response(status=status.HTTP_200_OK)
			else:
				return Response(status=status.HTTP_400_BAD_REQUEST)


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
				# Create AccountInfo first
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
					facebook=request.data.get('facebook', ''),
					telegram=request.data.get('telegram', ''),
				)
				# if user email duplicate, delete the AccountInfo just created and return 400
				try:
					user = Account.objects.create(
						email=request.data.get('email'),
						info_id=info.id,
						type=0,  # ICO Company
					)
				except:
					info.delete()
					return Response({'detail': 'User with this email already exists'}, status=status.HTTP_400_BAD_REQUEST)
				# if created user, add AccountInfo to team
				team.members.add(info)
				# give user just created a random password
				user.set_password(''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(16)]))
				user.save()

				user_verify_token = get_user_verify_token(user)

				if is_advisor:
					send_email(receiver_list=[user.email],
					           subject='ICOToday - ' + user.info.full_name() + ', Your Team is Waiting You',
					           template_name='TeamAdvisorInvitation',
					           ctx={'username': user.info.full_name(), 'token': user_verify_token.token, 'team_name': team.name}
					           )
				else:
					send_email(receiver_list=[user.email],
					           subject='ICOToday - ' + user.info.full_name() + ', Your Team is Waiting You',
					           template_name='TeamMemberInvitation',
					           ctx={'username': user.info.full_name(), 'token': user_verify_token.token, 'team_name': team.name}
					           )

				return Response(status=status.HTTP_200_OK)
			else:
				return Response(status=status.HTTP_400_BAD_REQUEST)
		# IMPORTANT: Here pk is Account Pk!
		elif request.method == 'DELETE':
			info = get_object_or_404(AccountInfo.objects.all(), pk=pk)
			info.team.members.remove(info)
			return Response(status=status.HTTP_200_OK)


class ExpertApplicationViewSet(viewsets.ViewSet):
	queryset = ExpertApplication.objects.all()
	parser_classes = (MultiPartParser, FormParser, JSONParser)
	permission_classes = (IsAuthenticated,)

	def retrieve(self, request):
		# Only Investor Allowed
		if request.user.type == 1:
			try:
				serializer = ExpertApplicationSerializer(request.user.expert_application)
				return Response(serializer.data, status=status.HTTP_200_OK)
			except ExpertApplication.DoesNotExist:
				return Response(status=status.HTTP_200_OK)
		else:
			return Response(status=status.HTTP_403_FORBIDDEN)

	def create(self, request):
		if request.data.get('detail'):
			ExpertApplication.objects.create(
				account_id=request.user.id,
				detail=request.data.get('detail')
			)
			return Response(status=status.HTTP_201_CREATED)
		else:
			return Response(status=status.HTTP_400_BAD_REQUEST)

	def update(self, request):
		try:
			application = request.user.expert_application
		except ExpertApplication.DoesNotExist:
			return Response(status=status.HTTP_200_OK)

		if request.data.get('detail'):
			application.detail = request.data.get('detail')
			application.save()
			serializer = ExpertApplicationSerializer(application)
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			return Response(status=status.HTTP_400_BAD_REQUEST)
