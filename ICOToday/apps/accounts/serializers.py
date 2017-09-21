# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from .models import Account, AccountInfo, ExpertApplication
from ..wallets.models import Wallet


class AccountInfoSerializer(serializers.ModelSerializer):
	"""
	Everything
	"""

	class Meta:
		model = AccountInfo
		fields = ['id', 'avatar', 'first_name', 'last_name', 'is_verified',
		          'company', 'title', 'description', 'interested',
		          'linkedin', 'twitter', 'telegram', 'facebook']


class BasicAccountInfoSerializer(serializers.ModelSerializer):
	class Meta:
		model = AccountInfo
		fields = ['id', 'avatar', 'first_name', 'last_name',
		          'company', 'title', 'description', 'is_advisor', 'is_expert',
		          'linkedin', 'twitter', 'telegram', 'facebook', 'account']


class MiniAccountInfoSerializer(serializers.ModelSerializer):
	"""
	Account info with name, avatar, and account id
	"""

	class Meta:
		model = AccountInfo
		fields = ['id', 'avatar', 'first_name', 'last_name', 'account']


class AuthAccountSerializer(serializers.ModelSerializer):
	"""
	Only For Register User
	"""

	class Meta:
		model = Account
		exclude = ('user_permissions', 'groups', 'is_superuser', 'is_staff', 'is_active', 'info')
		read_only_fields = ('created', 'updated',)
		write_only_fields = ('password',)

	def create(self, validated_data):
		if 'phone' in validated_data:
			account = Account(phone=validated_data['phone'], type=validated_data['type'])
		elif 'email' in validated_data:
			account = Account(email=validated_data['email'], type=validated_data['type'])
		else:
			return False

		account.set_password(validated_data['password'])
		info = AccountInfo.objects.create()
		account.info = info
		account.save()
		Wallet.objects.create(account_id=account.id)
		return account

	def update(self, instance, validated_data):
		instance.set_password(validated_data['password'])
		instance.save()
		return instance


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
