# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from models import Notification
from ..accounts.serializers import MiniAccountInfoSerializer


class NotificationSerializer(serializers.ModelSerializer):
	receiver = MiniAccountInfoSerializer()
	sender = MiniAccountInfoSerializer(allow_null=True)

	class Meta:
		model = Notification
		fields = ('id', 'receiver', 'sender', 'content', 'related',
		          'read', 'created',)
