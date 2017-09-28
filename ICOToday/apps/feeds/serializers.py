# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from .models import Feed

from ..accounts.serializers import MiniAccountInfoSerializer


class ReplySerializer(serializers.ModelSerializer):
	creator = MiniAccountInfoSerializer(read_only=True)

	class Meta:
		model = Feed
		fields = ['id', 'company_id', 'creator', 'content', 'created', 'updated', 'reply_to_id']
		read_only_fields = ('created', 'updated')

	def create(self, validated_data):
		validated_data['creator_id'] = self.context['creator_id']
		validated_data['company_id'] = self.context['company_id']
		validated_data['reply_to_id'] = self.context['reply_to_id']
		return Feed.objects.create(**validated_data)


class FeedSerializer(serializers.ModelSerializer):
	creator = MiniAccountInfoSerializer(read_only=True)
	replies = ReplySerializer(many=True, required=False, read_only=True)

	class Meta:
		model = Feed
		fields = ['id', 'company_id', 'rate', 'creator', 'content', 'created', 'updated', 'replies', 'type']
		read_only_fields = ('created', 'updated')

	def create(self, validated_data):
		validated_data['creator_id'] = self.context['creator_id']
		validated_data['company_id'] = self.context['company_id']
		return Feed.objects.create(**validated_data)
