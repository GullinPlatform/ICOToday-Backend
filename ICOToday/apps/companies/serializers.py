# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from .models import Company, PromotionApplication
from ..accounts.serializers import MiniAccountInfoSerializer


class BasicCompanySerializer(serializers.ModelSerializer):
	class Meta:
		model = Company
		fields = ['id', 'name', 'icon', 'description']
		read_only_fields = ['id']


class CompanySerializer(serializers.ModelSerializer):
	members = MiniAccountInfoSerializer(allow_null=True, many=True)

	class Meta:
		model = Company
		fields = ['id', 'name', 'icon', 'description', 'members', 'project']
		read_only_fields = ['id', 'members', 'project']


class PromotionApplicationSerializer(serializers.ModelSerializer):
	class Meta:
		model = PromotionApplication
		fields = '__all__'
		read_only_fields = ('created', 'updated')
