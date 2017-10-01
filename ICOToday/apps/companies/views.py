# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random
import string

from django.shortcuts import get_object_or_404
from django.db import Error

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from ..notifications.models import Notification
from ..accounts.serializers import AccountInfo, Account, BasicAccountInfoSerializer, MiniAccountInfoSerializer
from ..wallets.serializers import WalletSerializer, Wallet

from .serializers import Company, CompanySerializer, BasicCompanySerializer, PromotionApplication, PromotionApplicationSerializer

from ..utils.send_email import send_email
from ..utils.verify_token import VerifyTokenUtils


class CompanyViewSet(viewsets.ViewSet):
	queryset = Company.objects.all()
	parser_classes = (MultiPartParser, FormParser, JSONParser)
	permission_classes = (IsAuthenticatedOrReadOnly,)

	@staticmethod
	def _is_company_admin(account_info, company):
		if account_info.company_admin.id is company.id:
			return True
		else:
			return False

	def retrieve(self, request, company_id=None):
		company = get_object_or_404(self.queryset, id=company_id)
		serializer = CompanySerializer(company)
		return Response(serializer.data)

	def create(self, request):
		company = request.user.info.company
		if company:
			return Response({'detail': 'User can only have one company'}, status=status.HTTP_403_FORBIDDEN)
		if request.user.info.type != -1:
			return Response({'detail': 'User already set account type'}, status=status.HTTP_403_FORBIDDEN)

		if request.data.get('name'):
			wallet = Wallet.objects.create()
			company = Company.objects.create(
				name=request.data.get('name'),
				wallet=wallet
			)
			request.user.info.company = company
			request.user.info.company_admin = company  # Creator is company admin
			request.user.info.type = 0  # Change to Company User
			request.user.info.save()
			serializer = BasicCompanySerializer(company)
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		else:
			return Response(status=status.HTTP_400_BAD_REQUEST)

	def update(self, request, company_id=None):
		company = request.user.info.company
		if not company:
			return Response(status=status.HTTP_400_BAD_REQUEST)
		if not self._is_company_admin(request.user.info, company):
			return Response({'detail': 'Only company admin can add edit company page'}, status=status.HTTP_403_FORBIDDEN)

		serializer = CompanySerializer(company, data=request.data, partial=True)
		if serializer.is_valid():
			serializer.save()

		return Response(serializer.data, status=status.HTTP_200_OK)

	def members(self, request, company_id=None):
		company = get_object_or_404(self.queryset, id=company_id)
		serializer = BasicAccountInfoSerializer(company.members, many=True)
		return Response(serializer.data)

	def member_manage(self, request, account_info_id=None):
		# Check if user is company admin and does user have company
		company = request.user.info.company
		if not company:
			return Response(status=status.HTTP_400_BAD_REQUEST)
		if not self._is_company_admin(request.user.info, company):
			return Response({'detail': 'Only company admin can add company members'}, status=status.HTTP_403_FORBIDDEN)

		# Add Company Member to own company
		if request.method == 'POST':
			# Add New Company member and sent invite email
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
					company_id=request.user.info.company.id,
					is_advisor=is_advisor,
					linkedin=request.data.get('linkedin', ''),
					twitter=request.data.get('twitter', ''),
					facebook=request.data.get('facebook', ''),
					telegram=request.data.get('telegram', ''),
				)
				# if user email duplicate, delete the AccountInfo just created and return 400
				try:
					account = Account.objects.create(
						email=request.data.get('email'),
						info_id=info.id,
						type=0,  # ICO Company
					)
				except Error:
					info.delete()
					return Response({'detail': 'User with this email already exists'}, status=status.HTTP_400_BAD_REQUEST)

				# if created user, add AccountInfo to company
				company.members.add(info)
				# give user just created a random password
				account.set_password(''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(16)]))
				account.save()

				token_instance = VerifyTokenUtils.generate_token_by_user(user=account)
				if is_advisor:
					send_email(receiver_list=[account.email],
					           subject='ICOToday - ' + account.info.full_name() + ', Your Team is Waiting You',
					           template_name='TeamAdvisorInvitation',
					           ctx={'username': account.info.full_name(), 'token': token_instance.token, 'team_name': company.name}
					           )
				else:
					send_email(receiver_list=[account.email],
					           subject='ICOToday - ' + account.info.full_name() + ', Your Team is Waiting You',
					           template_name='TeamMemberInvitation',
					           ctx={'username': account.info.full_name(), 'token': token_instance.token, 'team_name': company.name}
					           )
				# Send back new account info
				serializer = MiniAccountInfoSerializer(account.info)
				return Response(serializer.data, status=status.HTTP_200_OK)
			# Add Existing User as Company Member
			elif account_info_id:
				info = get_object_or_404(AccountInfo.objects.all(), id=account_info_id)
				info.company = request.user.info.company
				info.save()
				Notification.objects.create(receiver_id=info.id,
				                            sender_id=request.user.info.id,
				                            content=company.name + ' has invited you to become their team member.',
				                            related='company')
				# send back new account info
				serializer = MiniAccountInfoSerializer(info)
				return Response(serializer.data, status=status.HTTP_200_OK)
			else:
				return Response(status=status.HTTP_400_BAD_REQUEST)

		# Remove Company Member from own company
		elif request.method == 'DELETE':
			info = get_object_or_404(AccountInfo.objects.all(), id=account_info_id)

			if self._is_company_admin(info, company):
				return Response({'detail': 'You cannot remove another admin'}, status=status.HTTP_403_FORBIDDEN)

			info.company.members.remove(info)
			info.type = 1  # Change to Investor User
			info.save()
			Notification.objects.create(receiver_id=info.id,
			                            sender_id=request.user.info.id,
			                            content=company.name + ' has removed you from their team member list.',
			                            related='company')
			return Response(status=status.HTTP_200_OK)

	def apply(self, request, company_id=None):
		# Apply to be Company Member
		company = get_object_or_404(self.queryset, id=company_id)
		company.pending_members.add(request.user.info)
		request.user.info.type = 1
		request.user.info.save()

		for admin in company.admins.all():
			Notification.objects.create(receiver_id=admin.id,
			                            sender_id=request.user.info.id,
			                            content='want to join the company.',
			                            related='user')
		return Response(status=status.HTTP_200_OK)

	def leave(self, request):
		company = request.user.info.company
		if not company:
			return Response(status=status.HTTP_400_BAD_REQUEST)
		if self._is_company_admin(request.user.info, company):
			return Response({'detail': 'Admin are unable to leave company'}, status=status.HTTP_403_FORBIDDEN)

		# Quit Company
		request.user.info.company = None
		request.user.info.type = 1  # Change to Investor User
		request.user.info.save()
		return Response(status=status.HTTP_200_OK)

	def member_application(self, request, account_infid=None):
		if not self._is_company_admin(request.user.info, request.user.info.company):
			return Response({'detail': 'Only company admin can add company members'}, status=status.HTTP_403_FORBIDDEN)

		# Approve team member application
		if request.method == 'POST':
			info = get_object_or_404(AccountInfo.objects.all(), id=account_info_id)
			info.company_pending = None
			info.company = request.user.info.company_admin
			info.type = 0  # Change to Company User
			info.save()
			Notification.objects.create(receiver_id=info.id,
			                            sender_id=request.user.info.id,
			                            content='You joined ' + info.company.name + '.',
			                            related='company')
			# Send new member back
			serializer = MiniAccountInfoSerializer(info)
			return Response(serializer.data, status=status.HTTP_200_OK)

		# Reject team member application
		elif request.method == 'DELETE':
			info = get_object_or_404(AccountInfo.objects.all(), id=account_info_id)
			info.company_pending = None
			info.type = 1  # Change to Investor User
			info.save()
			Notification.objects.create(receiver_id=info.id,
			                            sender_id=request.user.info.id,
			                            content='Your application to ' + info.company.name + ' is rejected.',
			                            related='company')
			return Response(status=status.HTTP_200_OK)

	def admins(self, request):
		if request.user.info.company:
			serializer = MiniAccountInfoSerializer(request.user.info.company.admins, many=True)
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			return Response({'detail': 'Your are not in a company'}, status=status.HTTP_403_FORBIDDEN)

	def admin_manage(self, request, account_info_id=None):
		if not self._is_company_admin(request.user.info, request.user.info.company):
			return Response({'detail': 'Only company admin can add company admins'}, status=status.HTTP_403_FORBIDDEN)
		info = get_object_or_404(AccountInfo.objects.all(), id=account_info_id)
		info.company_admin = request.user.info.company_admin
		info.save()
		# send back new account info
		serializer = MiniAccountInfoSerializer(info)
		return Response(serializer.data, status=status.HTTP_200_OK)

	def search(self, request):
		search_token = request.GET.get('token')
		if search_token:
			companies = self.queryset.filter(name__iregex=r'^' + search_token + r'+')
			serializer = BasicCompanySerializer(companies, many=True)
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			return Response(status=status.HTTP_200_OK)

	def wallet(self, request):
		company = request.user.info.company
		if not company:
			return Response(status=status.HTTP_400_BAD_REQUEST)
		if not self._is_company_admin(request.user.info, company):
			return Response({'detail': 'Only company admin can add company members'}, status=status.HTTP_403_FORBIDDEN)

		serializer = WalletSerializer(company.wallet)
		return Response(serializer.data, status=status.HTTP_200_OK)

	def promotion_application(self, request):
		if request.method == 'GET':
			company = request.user.info.company

			if not company or not company.promotion_applications.count():
				return Response(status=status.HTTP_400_BAD_REQUEST)

			serializer = PromotionApplicationSerializer(company.promotion_applications.first())
			return Response(serializer.data)

		elif request.method == 'POST':
			company = request.user.info.company
			if not company:
				return Response(status=status.HTTP_400_BAD_REQUEST)
			if not self._is_company_admin(request.user.info, company):
				return Response({'detail': 'Only company admin can submit promotion application'}, status=status.HTTP_403_FORBIDDEN)

			PromotionApplication.objects.create(
				company_id=company.id,
				duration=request.data.get('duration'),
				detail=request.data.get('detail'),
			)
			serializer = PromotionApplicationSerializer(company.promotion_applications.first())
			return Response(serializer.data)
