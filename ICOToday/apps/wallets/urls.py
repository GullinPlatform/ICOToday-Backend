# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

from .views import WalletViewSet, WalletStatViewSet

wallet_retrieve = WalletViewSet.as_view({
	'get': 'retrieve'
})

wallet_stat = WalletStatViewSet.as_view({
	'get': 'stat'
})

urlpatterns = [
	url(r'^$', wallet_retrieve, name='wallet_retrieve'),
	url(r'^stat/$', wallet_stat, name='wallet_stat'),
]
