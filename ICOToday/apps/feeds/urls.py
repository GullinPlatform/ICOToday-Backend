# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

from .views import FeedViewSet

feed = FeedViewSet.as_view({
	'get' : 'list',
	'post': 'create',
})

feed_reply = FeedViewSet.as_view({
	'post': 'reply',
})

feed_edit = FeedViewSet.as_view({
	'patch' : 'update',
	'delete': 'delete'
})

urlpatterns = [
	url(r'^(?P<project_id>[0-9]+)/$', feed, name='comment'),

	url(r'^(?P<comment_id>[0-9]+)/reply/$', feed_reply, name='comment_reply'),
	url(r'^(?P<comment_id>[0-9]+)/edit/$', feed_edit, name='comment_edit'),
]
