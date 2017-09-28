# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

from .views import ConversationViewSet

conversation = ConversationViewSet.as_view({
	'get' : 'retrieve_latest',
	'post': 'reply',
})

conversation_load_more = ConversationViewSet.as_view({
	'get': 'retrieve_more',
})

conversation_start_conversation = ConversationViewSet.as_view({
	'get': 'start_conversation',
})

conversation_read = ConversationViewSet.as_view({
	'post' : 'read'
})

urlpatterns = [
	url(r'^(?P<conversation_pk>[0-9]+)/$', conversation, name='conversation'),
	url(r'^ac/(?P<account_pk>[0-9]+)/$', conversation_start_conversation, name='conversation_start_conversation'),

	url(r'^(?P<conversation_pk>[0-9]+)/more/$', conversation_load_more, name='conversation_load_more'),
	url(r'^(?P<conversation_pk>[0-9]+)/read/$', conversation_read, name='conversation_read'),
]
