# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random
import string
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
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated

from .models import Account, VerifyToken, AccountInfo, ExpertApplication
from .serializers import AuthAccountSerializer, BasicAccountSerializer, BasicAccountInfoSerializer, AccountInfoSerializer, ExpertApplicationSerializer

from ..projects.models import Project, ProjectTag
from ..projects.serializers import ProjectSerializer

from ..notifications.models import Notification
from ..wallets.models import Wallet


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
	if user:
		try:
			token_instance = VerifyToken.objects.get(account_id=user.id)
			if token_instance.is_expired:
				return False
		except VerifyToken.DoesNotExist:
			return False
	elif token:
		try:
			token_instance = VerifyToken.objects.get(token=token)
			if token_instance.is_expired:
				return False
		except VerifyToken.DoesNotExist:
			return False
	else:
		return False

	token_instance.expire_time = timezone.now() - timedelta(days=10)
	token_instance.token = ''
	token_instance.save()
	return token_instance


def refresh_token(token=None):
	try:
		token_instance = VerifyToken.objects.get(token=token)
		token_instance.expire_time = timezone.now() + timedelta(days=1)
		token_instance.token = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(16)])
		token_instance.save()
		return token_instance
	except VerifyToken.DoesNotExist:
		return False


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

		user_verify_token = get_user_verify_token(account)

		send_email(receiver_list=[account.email],
		           subject='ICOToday - Email Verification',
		           template_name='EmailVerification',
		           ctx={'user': account, 'token': user_verify_token.token})

		return Response({'token': token}, status=status.HTTP_201_CREATED)

	def invited_register(self, request, token):
		# Check If token expired, if not return UserInfo
		if request.method == 'GET':
			token_instance = get_object_or_404(VerifyToken.objects.all(), token=token)
			if token_instance.is_expired:
				return Response({'detail': 'Token Expired'}, status=status.HTTP_400_BAD_REQUEST)
			serializer = BasicAccountSerializer(token_instance.account)
			return Response(serializer.data, status=status.HTTP_200_OK)

		# Invited Register AKA Change Password
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
			if request.user.is_authenticated:
				user_verify_token = get_user_verify_token(user=request.user)

				send_email(receiver_list=[request.user.email],
				           subject='ICOToday - Email Verification',
				           template_name='EmailVerification',
				           ctx={'user': request.user, 'token': user_verify_token}
				           )
				return Response(status=status.HTTP_200_OK)
			else:
				return Response(status=status.HTTP_400_BAD_REQUEST)

	def invite_email_resend(self, request, token=None):
		if not token:
			return Response(status=status.HTTP_400_BAD_REQUEST)

		user_verify_token = refresh_token(token=token)

		if user_verify_token:
			user = user_verify_token.account
			company = user.info.company.name
			if user.info.type == 2:  # Advisor
				send_email(receiver_list=[user.email],
				           subject='ICOToday - ' + user.info.full_name() + ', Your Team is Waiting You',
				           template_name='TeamAdvisorInvitation',
				           ctx={'username': user.info.full_name(), 'token': user_verify_token.token, 'team_name': company}
				           )
			else:
				send_email(receiver_list=[user.email],
				           subject='ICOToday - ' + user.info.full_name() + ', Your Team is Waiting You',
				           template_name='TeamMemberInvitation',
				           ctx={'username': user.info.full_name(), 'token': user_verify_token.token, 'team_name': company}
				           )
		return Response(status=status.HTTP_200_OK)

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

	def destroy(self, request, pk=None):
		if request.user.is_superuser or request.user.pk == int(pk):
			user = get_object_or_404(self.queryset, pk=pk)
			user.delete()
			return Response(status=status.HTTP_200_OK)
		else:
			return Response(status=status.HTTP_403_FORBIDDEN)

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

	def marked_posts(self, request, pk=None):
		if pk:  # Marked post from other user
			account = get_object_or_404(self.queryset, pk=pk)
			serializer = ProjectSerializer(account.info.marked_posts.all(), many=True)
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:  # Marked post from me
			serializer = ProjectSerializer(request.user.info.marked_posts.all(), many=True)
			return Response(serializer.data, status=status.HTTP_200_OK)

	# TODO : Add URL
	def add_interested(self, request):
		if not request.data.get('interested'):
			return Response(status=status.HTTP_400_BAD_REQUEST)

		for interest in request.data.get('interested'):
			tag = ProjectTag.objects.filter(tag=interest).first()
			if tag:
				request.user.info.interested.add(tag)
		return Response(status=status.HTTP_200_OK)

	# def created_posts(self, request, pk=None):

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

	def search(self, request, search_token):
		if search_token:
			if '@' in search_token:
				token = search_token.split("@")[0]
				accounts = AccountInfo.objects.filter(email__istartswith=token)
			else:
				tokens = search_token.split()
				accounts = AccountInfo.objects.filter(first_name__istartswith=tokens[0])
				accounts |= AccountInfo.objects.filter(last_name__istartswith=tokens[-1])

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
