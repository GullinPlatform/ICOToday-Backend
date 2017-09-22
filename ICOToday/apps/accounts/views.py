# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import check_password

from ..rest_framework_jwt.settings import api_settings
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Account, AccountInfo, ExpertApplication
from .serializers import AuthAccountSerializer, BasicAccountSerializer, BasicAccountInfoSerializer, AccountInfoSerializer, ExpertApplicationSerializer

from ..projects.models import ProjectTag
from ..projects.serializers import ProjectSerializer

from ..notifications.models import Notification
from ..wallets.models import Wallet

from ..utils.send_email import send_email
from ..utils.verify_token import VerifyTokenUtils


class AccountRegisterViewSet(viewsets.ViewSet):
	parser_classes = (MultiPartParser, FormParser, JSONParser)
	permission_classes = (AllowAny,)

	def register(self, request):
		serializer = AuthAccountSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		account = serializer.save()

		# If refer
		if request.data.get('referrer'):
			try:
				referrer = Account.objects.get(email=request.data.get('referrer'))
				referrer.wallet.icc_amount += 5
				referrer.save()
				Notification.objects.create(receiver_id=referrer.id,
				                            content='A friend just joined ICOToday with your referral link! 5 ICOCoins have been deposited to your wallet.',
				                            related='wallet')
			except Account.DoesNotExist or Wallet.DoesNotExist:
				pass

		account.info.wallet.icc_amount += 5
		account.info.wallet.save()
		Notification.objects.create(receiver_id=account.info.id,
		                            content='Welcome to ICOToday. As one of our early users, we have deposited 5 ICOCoins to your wallet.',
		                            related='wallet')

		# return token right away
		jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
		jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
		payload = jwt_payload_handler(account)
		token = jwt_encode_handler(payload)

		user_verify_token = VerifyTokenUtils.generate_token_by_user(user=account)

		send_email(receiver_list=[account.email],
		           subject='ICOToday - Email Verification',
		           template_name='EmailVerification',
		           ctx={'user': account, 'token': user_verify_token.token})

		return Response({'token': token}, status=status.HTTP_201_CREATED)

	def invited_register(self, request, token):
		# Check If token expired, if not return UserInfo
		if request.method == 'GET':
			token_instance = VerifyTokenUtils.get_token_by_token(token=token)
			if not VerifyTokenUtils.validate_token(token_instance=token_instance):
				return Response({'detail': 'Token Expired'}, status=status.HTTP_400_BAD_REQUEST)

			serializer = BasicAccountSerializer(token_instance.account)
			return Response(serializer.data, status=status.HTTP_200_OK)

		# Invited Register AKA Change Password
		elif request.method == 'POST':
			if request.data.get('password'):
				# Get token instance
				token_instance = VerifyTokenUtils.get_token_by_token(token=token)
				# Validate token
				if VerifyTokenUtils.validate_token(token_instance=token_instance):
					# Expire token
					VerifyTokenUtils.expire_token(token_instance=token_instance)
					token_instance.account.set_password(request.data.get('password'))
					token_instance.account.save()
					token_instance.account.info.is_verified = True
					token_instance.account.info.save()

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

			# Get token instance
			token_instance = VerifyTokenUtils.get_token_by_token(token=token)
			# Validate token
			if VerifyTokenUtils.validate_token(token_instance=token_instance):
				# Expire token
				VerifyTokenUtils.expire_token(token_instance=token_instance)
			else:
				return Response({'message': 'Token Invalid'}, status=status.HTTP_400_BAD_REQUEST)

			token_instance.account.info.is_verified = True
			token_instance.account.info.save()

			return Response(status=status.HTTP_200_OK)
		# Resend Verify Email
		elif request.method == 'POST':
			if request.user.is_authenticated and not request.user.info.is_verified:
				token_instance = VerifyTokenUtils.get_token_by_user(user=request.user)
				# If Expire token
				if not VerifyTokenUtils.validate_token(token_instance=token_instance):
					# Refresh token
					VerifyTokenUtils.refresh_token(token_instance=token_instance)

				send_email(receiver_list=[request.user.email],
				           subject='ICOToday - Email Verification',
				           template_name='EmailVerification',
				           ctx={'user': request.user, 'token': token_instance.token}
				           )
				return Response(status=status.HTTP_200_OK)
			else:
				return Response(status=status.HTTP_400_BAD_REQUEST)

	def invite_email_resend(self, request, token=None):
		if not token:
			return Response(status=status.HTTP_400_BAD_REQUEST)

		token_instance = VerifyTokenUtils.get_token_by_user(user=request.user)
		# If Expire token
		if not VerifyTokenUtils.validate_token(token_instance=token_instance):
			# Refresh token
			VerifyTokenUtils.refresh_token(token_instance=token_instance)

		if token_instance:
			user = token_instance.account
			company = user.info.company.name
			if user.info.type == 2:  # Advisor
				send_email(receiver_list=[user.email],
				           subject='ICOToday - ' + user.info.full_name() + ', Your Team is Waiting You',
				           template_name='TeamAdvisorInvitation',
				           ctx={'username': user.info.full_name(), 'token': token_instance.token, 'team_name': company}
				           )
			else:
				send_email(receiver_list=[user.email],
				           subject='ICOToday - ' + user.info.full_name() + ', Your Team is Waiting You',
				           template_name='TeamMemberInvitation',
				           ctx={'username': user.info.full_name(), 'token': token_instance.token, 'team_name': company}
				           )
		return Response(status=status.HTTP_200_OK)

	def forget_password(self, request, token=None):
		# verify token
		if request.method == 'GET':
			# Get token by token
			token_instance = VerifyTokenUtils.get_token_by_token(token=token)
			# Validate
			if VerifyTokenUtils.validate_token(token_instance=token_instance):
				return Response(status=status.HTTP_200_OK)
			else:
				return Response({'detail': 'Token Invalid'}, status=status.HTTP_400_BAD_REQUEST)

		# send email
		if request.method == 'POST':
			email = request.data.get('email')
			if not email:
				return Response(status=status.HTTP_400_BAD_REQUEST)

			token_instance = VerifyTokenUtils.generate_token_by_email(email=email)

			send_email(receiver_list=[email],
			           subject='ICOToday - Password Reset',
			           template_name='PasswordReset',
			           ctx={'token': token_instance.token}
			           )
			return Response(status=status.HTTP_200_OK)

		# change password
		elif request.method == 'PUT':
			# if token not exist return 404 here
			token_instance = VerifyTokenUtils.get_token_by_token(token=token)

			if not VerifyTokenUtils.validate_token(token_instance=token_instance):
				return Response({'detail': 'Token Invalid'}, status=status.HTTP_400_BAD_REQUEST)
			else:
				# set new password to user
				token_instance.account.set_password(request.data['password'])
				token_instance.account.save()
				VerifyTokenUtils.expire_token(token_instance=token_instance)
				return Response(status=status.HTTP_200_OK)

	def logout(self, request):
		from ..rest_framework_jwt.settings import api_settings
		response = Response()
		response.delete_cookie(api_settings.JWT_AUTH_COOKIE)
		return response


class AccountViewSet(viewsets.ViewSet):
	queryset = Account.objects.exclude(is_staff=1)
	parser_classes = (MultiPartParser, FormParser, JSONParser)
	permission_classes = (IsAuthenticated,)

	# TODO link url
	def register_follow_up(self, request):
		if not request.data.get('type'):
			return Response(status=status.HTTP_400_BAD_REQUEST)

		if request.data.get('type') == 0:  # Company
			request.user.info.type = 0
			request.user.info.save()
		else:  # All others go Investor first
			request.user.info.type = 1
			request.user.info.save()

	def retrieve(self, request, pk):
		user = get_object_or_404(self.queryset, pk=pk)
		serializer = BasicAccountSerializer(user)
		return Response(serializer.data)

	def me(self, request):
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

	def change_password(self, request):
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

	def marked_projects(self, request, pk=None):
		if pk:  # Marked post from other user
			account = get_object_or_404(self.queryset, pk=pk)
			serializer = ProjectSerializer(account.info.marked_projects.all(), many=True)
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:  # Marked post from me
			serializer = ProjectSerializer(request.user.info.marked_projects.all(), many=True)
			return Response(serializer.data, status=status.HTTP_200_OK)

	def add_interests(self, request):
		"""
		request.data:
		interests: list of string
		"""
		if not request.data.get('interests'):
			return Response(status=status.HTTP_400_BAD_REQUEST)

		for interest in request.data.get('interests'):
			tag = ProjectTag.objects.filter(tag=interest).first()
			if tag:
				request.user.info.interests.add(tag)
		return Response(status=status.HTTP_200_OK)

	def two_factor_auth(self, request):
		# Send Email
		if request.method == 'POST':
			token_instance = VerifyTokenUtils.generate_token_by_user(user=request.user, only_digit=True)
			send_email(receiver_list=[request.user.email],
			           subject='ICOToday - Verification Token',
			           template_name='TwoFactorAuth',
			           ctx={'token': token_instance.token})
			return Response(status=status.HTTP_200_OK)

		# Verify 2 Factor Auth Token
		elif request.method == 'GET':
			token_instance1 = VerifyTokenUtils.get_token_by_user(user=request.user)
			token_instance2 = VerifyTokenUtils.get_token_by_token(token=request.data.get('token'))

			if token_instance1.id == token_instance2.id and VerifyTokenUtils.validate_token(token_instance=token_instance1):
				VerifyTokenUtils.expire_token(token_instance=token_instance1)
				return Response(status=status.HTTP_200_OK)
			else:
				return Response({'detail': 'Token Invalid'}, status=status.HTTP_400_BAD_REQUEST)

	def search(self, request):
		"""
		request.get:
		search: string
		"""
		search_token = request.GET.get('search')
		if search_token:
			if '@' in search_token:
				token = search_token.split("@")[0]
				accounts = self.queryset.filter(email__iregex=r'^' + token + r'+')
			else:
				queryset = AccountInfo.objects.all()
				# Cache query in memory to improve performance
				[q for q in queryset]
				tokens = search_token.split()
				accounts = queryset.filter(first_name__iregex=r'^' + tokens[0] + r'+')
				accounts |= queryset.filter(last_name__iregex=r'^' + tokens[-1] + r'+')

			serializer = BasicAccountInfoSerializer(accounts, many=True)
			return Response(serializer.data)
		else:
			return Response(status=status.HTTP_400_BAD_REQUEST)


class ExpertApplicationViewSet(viewsets.ViewSet):
	queryset = ExpertApplication.objects.all()
	parser_classes = (MultiPartParser, FormParser, JSONParser)
	permission_classes = (IsAuthenticated,)

	def retrieve(self, request):
		# Only Investor Allowed
		if request.user.info.type == 1:
			try:
				serializer = ExpertApplicationSerializer(request.user.info.expert_application)
				return Response(serializer.data, status=status.HTTP_200_OK)
			except ExpertApplication.DoesNotExist:
				return Response(status=status.HTTP_200_OK)
		else:
			return Response(status=status.HTTP_403_FORBIDDEN)

	def create(self, request):
		if request.data.get('detail'):
			ExpertApplication.objects.create(
				account_id=request.user.info.id,
				detail=request.data.get('detail')
			)
			return Response(status=status.HTTP_201_CREATED)
		else:
			return Response(status=status.HTTP_400_BAD_REQUEST)

	def update(self, request):
		try:
			application = request.user.info.expert_application
		except ExpertApplication.DoesNotExist:
			return Response(status=status.HTTP_400_BAD_REQUEST)

		if request.data.get('detail'):
			application.detail = request.data.get('detail')
			application.save()
			serializer = ExpertApplicationSerializer(application)
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			return Response(status=status.HTTP_400_BAD_REQUEST)
