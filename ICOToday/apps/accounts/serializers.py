# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from .models import Account, AccountInfo, ExpertApplication
from ..wallets.models import Wallet
from ..companies.models import Company


# For circular requirements
class MiniCompanySerializer(serializers.ModelSerializer):
	class Meta:
		model = Company
		fields = ['id', 'name', 'project']


class AccountInfoSerializer(serializers.ModelSerializer):
	"""
	Everything
	"""
	company = MiniCompanySerializer(read_only=True)
	company_admin = MiniCompanySerializer(read_only=True)

	class Meta:
		model = AccountInfo
		fields = ['id', 'account', 'type', 'avatar', 'first_name', 'last_name', 'full_name',
		          'company', 'company_admin', 'title', 'description', 'interests', 'is_verified',
		          'linkedin', 'twitter', 'telegram', 'facebook']
		read_only_fields = ('type', 'is_verified', 'interests', 'id', 'full_name')


class BasicAccountInfoSerializer(serializers.ModelSerializer):
	"""
	Account info with id, account_id, name, avatar, title, description and social media info
	"""
	company = MiniCompanySerializer(read_only=True)

	class Meta:
		model = AccountInfo
		fields = ['id', 'avatar', 'full_name', 'account', 'title', 'description', 'company',
		          'linkedin', 'twitter', 'telegram', 'facebook', 'type']


class MiniAccountInfoSerializer(serializers.ModelSerializer):
	"""
	Account info with name, avatar, and account id
	"""

	class Meta:
		model = AccountInfo
		fields = ['id', 'avatar', 'full_name', 'account', 'title']


class AuthAccountSerializer(serializers.ModelSerializer):
	"""
	Only For Register User
	"""

	class Meta:
		model = Account
		exclude = ('user_permissions', 'groups', 'is_superuser', 'is_staff', 'info')
		read_only_fields = ('created', 'updated',)
		write_only_fields = ('password',)

	def create(self, validated_data):
		if 'phone' in validated_data:
			account = Account(phone=validated_data['phone'])
		elif 'email' in validated_data:
			account = Account(email=validated_data['email'])
		else:
			return False

		account.set_password(validated_data['password'])
		wallet = Wallet.objects.create()
		info = AccountInfo.objects.create(wallet=wallet)
		account.info = info
		account.save()
		return account


class BasicAccountSerializer(serializers.ModelSerializer):
	"""
	Everything
	"""
	info = AccountInfoSerializer()

	class Meta:
		model = Account
		fields = ['id', 'email', 'phone', 'info']


class ExpertApplicationSerializer(serializers.ModelSerializer):
	"""
	Everything
	"""

	class Meta:
		model = ExpertApplication
		fields = '__all__'
		read_only_fields = ('created', 'updated',)
