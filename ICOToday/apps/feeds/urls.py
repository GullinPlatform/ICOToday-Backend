# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

from .views import FeedViewSet

feed = FeedViewSet.as_view({
	'post': 'create',
})

feed_reply = FeedViewSet.as_view({
	'post': 'reply',
})

feed_delete = FeedViewSet.as_view({
	'delete': 'delete'
})

my_feeds = FeedViewSet.as_view({
	'get': 'my_feeds',
})

project_feeds = FeedViewSet.as_view({
	'get': 'project_feeds',
})

user_feeds = FeedViewSet.as_view({
	'get': 'user_feeds',
})

urlpatterns = [
	url(r'^new/$', feed, name='feed'),
	url(r'^(?P<feed_id>[0-9]+)/delete/$', feed_delete, name='feed-delete'),
	url(r'^(?P<feed_id>[0-9]+)/reply/$', feed_reply, name='feed-reply'),

	url(r'^my/$', my_feeds, name='my-feed'),
	url(r'^project/(?P<project_id>[0-9]+)$', project_feeds, name='project-feed'),
	url(r'^user/(?P<account_info_id>[0-9]+)$', user_feeds, name='account_info_id-feed'),
]
