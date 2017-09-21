# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets, status
from rest_framework.response import Response

from models import Notification
from serializers import NotificationSerializer


class NotificationViewSet(viewsets.ViewSet):
	queryset = Notification.objects.exclude(read=True)
	serializer_class = NotificationSerializer
	# Permission set
	permission_classes = (permissions.IsAuthenticated,)

	def fetch(self, request):
		"""
		Only Return unread notifications
		"""
		notifications = self.queryset.filter(receiver_id=request.user.info.id, read=False)
		serializer = NotificationSerializer(notifications, many=True)
		return Response(serializer.data)

	def list(self, request, page=0):
		"""
		Return 20 notifications each time (including read and unread)
		"""
		notifications = self.queryset.filter(receiver_id=request.user.info.id)[page * 20: (page + 1) * 20]
		serializer = NotificationSerializer(notifications, many=True)
		return Response(serializer.data)

	def read(self, request, id):
		notification = get_object_or_404(self.queryset, id=id)
		notification.read = True
		notification.save()
		return Response(status=status.HTTP_200_OK)
