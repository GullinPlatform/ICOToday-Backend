# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from .models import Company, PromotionApplication
from ..accounts.serializers import MiniAccountInfoSerializer


class BasicCompanySerializer(serializers.ModelSerializer):
	class Meta:
		model = Company
		fields = ['id', 'name', 'project']
		read_only_fields = ['id']


class CompanySerializer(serializers.ModelSerializer):
	members = MiniAccountInfoSerializer(allow_null=True, many=True)

	class Meta:
		model = Company
		fields = ['id', 'name', 'members', 'project']
		read_only_fields = ['id', 'members', 'project']


class PromotionApplicationSerializer(serializers.ModelSerializer):
	class Meta:
		model = PromotionApplication
		fields = ['company', 'duration', 'detail', 'status']
		read_only_fields = ('created', 'updated')