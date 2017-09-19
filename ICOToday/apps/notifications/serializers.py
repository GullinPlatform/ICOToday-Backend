from rest_framework import serializers

from models import Notification
from ..accounts.serializers import BasicAccountSerializer


class NotificationSerializer(serializers.ModelSerializer):
	receiver = BasicAccountSerializer()
	sender = BasicAccountSerializer(allow_null=True)

	class Meta:
		model = Notification
		fields = ('id', 'content', 'read', 'created', 'receiver', 'sender', 'related_link')
