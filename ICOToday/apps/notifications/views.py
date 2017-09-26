# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets, status
from rest_framework.response import Response

from models import Notification
from serializers import NotificationSerializer


class NotificationViewSet(viewsets.ViewSet):
	queryset = Notification.objects.exclude()
	serializer_class = NotificationSerializer
	# Permission set
	permission_classes = (permissions.IsAuthenticated,)

	def fetch(self, request, page=0):
		"""
		Return top 10 unread notifications each time
		"""
		notifications = self.queryset.filter(receiver_id=request.user.info.id, read=False)[page * 10: (page + 1) * 10]
		serializer = NotificationSerializer(notifications, many=True)
		return Response(serializer.data)

	def fetch_read(self, request, page=0):
		"""
		Return top 10 read notifications each time
		"""
		notifications = self.queryset.filter(receiver_id=request.user.info.id, read=True)[page * 10: (page + 1) * 10]
		serializer = NotificationSerializer(notifications, many=True)
		return Response(serializer.data)

	def fetch_all(self, request, page=0):
		"""
		Return 10 notifications each time (including read and unread)
		"""
		notifications = self.queryset.filter(receiver_id=request.user.info.id)[page * 10: (page + 1) * 10]
		serializer = NotificationSerializer(notifications, many=True)
		return Response(serializer.data)

	def read(self, request, id):
		"""
		Mark notification as read
		"""
		notification = get_object_or_404(self.queryset, id=id)
		notification.read = True
		notification.save()
		return Response(status=status.HTTP_200_OK)

	def read_all(self, request):
		"""
		Mark all notifications as read
		"""
		notifications = request.user.info.notifications.all()
		for notification in notifications:
			if not notification.read:
				notification.read = True
				notification.save()
		return Response(status=status.HTTP_200_OK)
