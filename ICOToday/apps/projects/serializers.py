# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from .models import Project, ProjectTag, ProjectRatingDetail

from ..companies.serializers import BasicCompanySerializer
from ..accounts.serializers import MiniAccountInfoSerializer


class ProjectTagSerializer(serializers.ModelSerializer):
	class Meta:
		model = ProjectTag
		fields = ['tag']


class ProjectSerializer(serializers.ModelSerializer):
	tags = ProjectTagSerializer(required=False, allow_null=True, many=True, read_only=True)
	company = BasicCompanySerializer(required=False, allow_null=True, read_only=True)

	class Meta:
		model = Project
		exclude = ['marked']
		read_only_fields = ['created', 'updated', 'status']


class BasicProjectSerializer(serializers.ModelSerializer):
	tags = ProjectTagSerializer(required=False, allow_null=True, many=True)
	company = BasicCompanySerializer(allow_null=True)

	class Meta:
		model = Project
		fields = ['id', 'company', 'description_short', 'rating',
		          'logo_image', 'promote_image', 'name', 'type', 'category',
		          'status', 'tags', 'website', 'maximum_goal', 'minimum_goal', 'coin_unit', 'accept',
		          'start_datetime', 'end_datetime', 'current', 'money_raised', 'equality_on_offer',
		          'medium', 'twitter', 'slack', 'telegram']
		read_only_fields = ['created', 'updated', 'status']


class MiniProjectSerializer(serializers.ModelSerializer):
	class Meta:
		model = Project
		fields = ['id', 'company', 'description_short', 'logo_image', 'rating']


class ProjectRatingDetailSerializer(serializers.ModelSerializer):
	rater = MiniAccountInfoSerializer()

	class Meta:
		model = ProjectRatingDetail
		fields = '__all__'
