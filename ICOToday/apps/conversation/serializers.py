# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from .models import Message, Conversation

from ..accounts.serializers import MiniAccountInfoSerializer


class MessageSerializer(serializers.ModelSerializer):
	creator = MiniAccountInfoSerializer(read_only=True)

	class Meta:
		model = Message
		fields = ['id', 'sender', 'receiver', 'read', 'created', 'updated']
		read_only_fields = ('created', 'updated')
