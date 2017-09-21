# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random
import string

from datetime import timedelta

from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from ..accounts.models import AccountInfo, Account, VerifyToken

from .models import Company
from .serializers import CompanySerializer, BasicCompanySerializer


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


class CompanyViewSet(viewsets.ViewSet):
	queryset = Company.objects.all()
	parser_classes = (MultiPartParser, FormParser, JSONParser)
	permission_classes = (IsAuthenticatedOrReadOnly,)

	def list(self, request):
		serializer = BasicCompanySerializer(self.queryset, many=True)
		return Response(serializer.data)

	def retrieve(self, request, pk=None):
		company = get_object_or_404(self.queryset, pk=pk)
		serializer = CompanySerializer(company)
		return Response(serializer.data)

	def create(self, request):
		if request.data.get('name') and request.data.get('description'):
			company = Company.objects.create(
				name=request.data.get('name'),
				description=request.data.get('description')
			)
			request.user.company = company
			request.use.save()
			return Response(status=status.HTTP_201_CREATED)
		else:
			return Response(status=status.HTTP_400_BAD_REQUEST)

	def update(self, request, pk):
		company = get_object_or_404(self.queryset, pk=pk)

		if request.data.get('name'):
			company.name = request.data.get('name')

		if request.data.get('description'):
			company.description = request.data.get('description')

			company.save()
		return Response(status=status.HTTP_200_OK)

	def add_company_member(self, request, pk):
		# IMPORTANT: Here pk is Company Pk!
		if request.method == 'PATCH':
			company = get_object_or_404(self.queryset, pk=pk)
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
					company_id=pk,
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

				# if created user, add AccountInfo to company
				company.members.add(info)
				# give user just created a random password
				user.set_password(''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(16)]))
				user.save()

				user_verify_token = get_user_verify_token(user)

				if is_advisor:
					send_email(receiver_list=[user.email],
					           subject='ICOToday - ' + user.info.full_name() + ', Your Team is Waiting You',
					           template_name='TeamAdvisorInvitation',
					           ctx={'username': user.info.full_name(), 'token': user_verify_token.token, 'team_name': company.name}
					           )
				else:
					send_email(receiver_list=[user.email],
					           subject='ICOToday - ' + user.info.full_name() + ', Your Team is Waiting You',
					           template_name='TeamMemberInvitation',
					           ctx={'username': user.info.full_name(), 'token': user_verify_token.token, 'team_name': company.name}
					           )

				return Response(status=status.HTTP_200_OK)
			else:
				return Response(status=status.HTTP_400_BAD_REQUEST)
		# IMPORTANT: Here pk is Account Pk!
		elif request.method == 'DELETE':
			info = get_object_or_404(AccountInfo.objects.all(), pk=pk)
			info.company.members.remove(info)
			return Response(status=status.HTTP_200_OK)

	# TODO: add company admin
	def add_company_admin(self, request):
		pass

	# TODO: search by company name
	def search(self, request, search_token):
		pass

	# post feed shouldn't be here, should be in feeds
	# def feed(self, request):
	# 	pass
