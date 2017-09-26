# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

from .views import NotificationViewSet

notification_fetch = NotificationViewSet.as_view({
	'get': 'fetch'
})
notification_fetch_read = NotificationViewSet.as_view({
	'get': 'fetch_read'
})
notification_fetch_all = NotificationViewSet.as_view({
	'get': 'fetch_all'
})

notification_read = NotificationViewSet.as_view({
	'post': 'read'
})
notification_read_all = NotificationViewSet.as_view({
	'post': 'read_all'
})

urlpatterns = [
	url(r'^fetch/$', notification_fetch, name='notification-fetch-unread'),
	url(r'^fetch/(?P<page>[0-9]+)/$', notification_fetch, name='notification-fetch-unread'),

	url(r'^fetch/read/$', notification_fetch_read, name='notification-fetch-read'),
	url(r'^fetch/read/(?P<page>[0-9]+)/$', notification_fetch_read, name='notification-fetch-read'),

	url(r'^fetch/all/$', notification_fetch_all, name='notification-fetch-all'),
	url(r'^fetch/all/(?P<page>[0-9]+)/$', notification_fetch_all, name='notification-fetch-all'),

	url(r'^read/(?P<id>[0-9]+)/$', notification_read, name='notification-read'),
	url(r'^read/all/$', notification_read_all, name='notification-read-all'),
]
