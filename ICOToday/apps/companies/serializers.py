# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from .models import Company, PromotionApplication
from ..accounts.serializers import BasicAccountInfoSerializer


class BasicCompanySerializer(serializers.ModelSerializer):
	class Meta:
		model = Company
		fields = ['id', 'name', 'company_icon', 'description']
		read_only_fields = ('created', 'updated',)


class CompanySerializer(serializers.ModelSerializer):
	members = BasicAccountInfoSerializer(allow_null=True, many=True)

	class Meta:
		model = Company
		fields = ['id', 'name', 'company_icon', 'description', 'members']
		read_only_fields = ('created', 'updated',)


class PromotionApplicationSerializer(serializers.ModelSerializer):
	class Meta:
		model = PromotionApplication
		fields = '__all__'
		read_only_fields = ('created', 'updated')
