# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import check_password
from django.contrib.gis.geoip2 import GeoIP2
from django.conf import settings

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly

from .serializers import Account, AccountInfo, ExpertApplication, AuthAccountSerializer, BasicAccountSerializer, MiniAccountInfoSerializer, AccountInfoSerializer, ExpertApplicationSerializer, \
	BasicAccountInfoSerializer
from ..projects.serializers import ProjectTag, ProjectSerializer

from ..notifications.models import Notification

from ..utils.send_email import send_email
from ..utils.verify_token import VerifyTokenUtils
from ..utils.google_recaptcha import recaptcha_verify
from ..utils.return_auth_token import return_auth_token
from ..utils.get_client_ip import get_client_ip


class AccountRegisterViewSet(viewsets.ViewSet):
	parser_classes = (MultiPartParser, FormParser, JSONParser)
	permission_classes = (AllowAny,)

	def register(self, request):
		# Validate Google reCAPTCHA
		# if not recaptcha_verify(request):
		# 	return Response(status=status.HTTP_400_BAD_REQUEST)
		ip = get_client_ip(request)

		serializer = AuthAccountSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		account = serializer.save()

		account.info.first_name = request.data.get('first_name', None)
		account.info.last_name = request.data.get('last_name', None)
		account.info.last_login_ip = ip
		account.info.whitelist = request.data.get('whitelist', False)
		account.info.amount_to_invest = request.data.get('amount_to_invest', 0)
		account.info.save()

		# If refer
		if request.data.get('referrer'):
			referrer = Account.objects.filter(email=request.data.get('referrer')).first()
			if referrer:
				referrer.info.wallet.ict_amount += 5
				referrer.info.wallet.save()
				Notification.objects.create(sender_id=settings.OFFICIAL_ACCOUNT_INFO_ID,
				                            receiver_id=referrer.info.id,
				                            content='A friend just joined ICOToday with your referral link! 5 ICOTokens have been deposited to your wallet.',
				                            related='wallet')

		# Add Bonny to User Wallet
		account.info.wallet.ict_amount += 5
		account.info.wallet.save()
		Notification.objects.create(sender_id=settings.OFFICIAL_ACCOUNT_INFO_ID,
		                            receiver_id=account.info.id,
		                            content='Welcome to ICOToday. As one of our early users, we have deposited 5 ICOTokens to your wallet.',
		                            related='wallet')

		# Send Verification Email
		user_verify_token = VerifyTokenUtils.generate_token_by_user(user=account)
		send_email(receiver_list=[account.email],
		           subject='ICOToday - Email Verification',
		           template_name='EmailVerification',
		           ctx={'username': account.info.full_name(), 'token': user_verify_token.token})

		# Use utils to set token in cookie in response
		return return_auth_token(account)

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

			# Check form data
			if not request.data.get('password'):
				return Response({'detail': 'No password provided'}, status=status.HTTP_400_BAD_REQUEST)

			# Get token instance
			token_instance = VerifyTokenUtils.get_token_by_token(token=token)

			# Validate token
			if not VerifyTokenUtils.validate_token(token_instance=token_instance):
				return Response({'detail': 'Token Invalid'}, status=status.HTTP_400_BAD_REQUEST)

			# Expire token
			VerifyTokenUtils.expire_token(token_instance=token_instance)
			account = token_instance.account

			# Set account password
			account.set_password(request.data.get('password'))
			account.save()

			# Update user info
			ip = get_client_ip(request)
			account.info.is_verified = True
			account.info.last_login_ip = ip
			account.info.save()

			# Add Bonny to User Wallet
			account.info.wallet.ict_amount += 5
			account.info.wallet.save()
			Notification.objects.create(sender_id=settings.OFFICIAL_ACCOUNT_INFO_ID,
			                            receiver_id=account.info.id,
			                            content='Welcome to ICOToday. As one of our early users, we have deposited 5 ICOTokens to your wallet.',
			                            related='wallet')

			# Use utils to set token in cookie in response
			return return_auth_token(account)

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
				           ctx={'user': request.user.info.full_name(), 'token': token_instance.token})
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
		response = Response()
		response.delete_cookie('icotodaytoken')
		return response

	def stat(self, request):
		count = Account.objects.count()
		return Response({'count': count})


class AccountViewSet(viewsets.ViewSet):
	queryset = Account.objects.all()
	account_info_queryset = AccountInfo.objects.all()
	parser_classes = (MultiPartParser, FormParser, JSONParser)
	permission_classes = (IsAuthenticatedOrReadOnly,)

	def log_ip(self, request):
		ip = get_client_ip(request)
		if ip != request.user.info.last_login_ip:
			request.user.info.last_login_ip = ip
			request.user.info.save()
			g = GeoIP2()
			city = g.city(ip)
			location = city.get('city') + ', ' + city.get('country_name')

			send_email([request.user.email],
			           'ICOToday - Login from different IP',
			           'DifferentIP',
			           {'username': request.user.info.full_name(),
			            'ip'      : ip,
			            'location': location})
		return Response(status=status.HTTP_200_OK)

	def set_account_type(self, request):
		if request.data.get('type', None) is None:
			return Response(status=status.HTTP_400_BAD_REQUEST)

		if request.data.get('type') == 0:  # Company
			request.user.info.type = 0
			request.user.info.save()
		else:  # All others go Investor first
			request.user.info.type = 1
			request.user.info.save()
		return Response(status=status.HTTP_200_OK)

	def retrieve(self, request, id):
		user = get_object_or_404(self.queryset, id=id)
		serializer = BasicAccountSerializer(user)
		return Response(serializer.data)

	def retrieve_info(self, request, account_info_id):
		user = get_object_or_404(self.account_info_queryset, id=account_info_id)
		serializer = AccountInfoSerializer(user)
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
				data = request.data.copy()
				del data['interests']
				del data['account']
				del data['is_verified']
				del data['company']
				del data['type']
				del data['id']
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

	def marked_projects(self, request, id=None):
		if id:  # Marked post from other user
			account_info = get_object_or_404(self.account_info_queryset, id=id)
			serializer = ProjectSerializer(account_info.marked_projects.all(), many=True)
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

			serializer = MiniAccountInfoSerializer(accounts, many=True)
			return Response(serializer.data)
		else:
			return Response(status=status.HTTP_400_BAD_REQUEST)

	def follow(self, request, account_info_id=None):
		if request.method == 'POST':
			account_info = get_object_or_404(self.account_info_queryset, id=account_info_id)
			request.user.info.followings.add(account_info)
			serializer = BasicAccountInfoSerializer(account_info)
			return Response(serializer.data, status=status.HTTP_200_OK)

		elif request.method == 'DELETE':
			account_info = get_object_or_404(self.account_info_queryset, id=account_info_id)
			request.user.info.followings.remove(account_info)
			return Response(status=status.HTTP_200_OK)

	def followings(self, request, account_info_id=None):
		if account_info_id:
			account_info = get_object_or_404(self.account_info_queryset, id=account_info_id)
			serializer = BasicAccountInfoSerializer(account_info.followings, many=True)
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			serializer = BasicAccountInfoSerializer(request.user.info.followings, many=True)
			return Response(serializer.data, status=status.HTTP_200_OK)

	def followers(self, request, account_info_id=None):
		if account_info_id:
			account_info = get_object_or_404(self.account_info_queryset, id=account_info_id)
			serializer = BasicAccountInfoSerializer(account_info.followers, many=True)
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			serializer = BasicAccountInfoSerializer(request.user.info.followers, many=True)
			return Response(serializer.data, status=status.HTTP_200_OK)

	def experts_list(self, request):
		experts = self.account_info_queryset.filter(type=2)
		serializer = BasicAccountInfoSerializer(experts, many=True)
		# TODO: return expert count at the same time
		return Response(serializer.data, status=status.HTTP_200_OK)


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
				detail=unicode(request.data.get('detail')),
				resume=request.data.get('resume'),
				previous_rating_example=request.data.get('past_rating_example'),
			)
			if request.data.get('linkedin'):
				request.user.info.linkedin = request.data.get('linkedin')
				request.user.info.save()

			Notification.objects.create(sender_id=settings.OFFICIAL_ACCOUNT_INFO_ID,
			                            receiver_id=request.user.info.id,
			                            content='Thank you for submitting your analyst application on ICOToday! We are reviewing your application.',
			                            related='expert_app')
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
