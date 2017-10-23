# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

from .views import WalletViewSet

wallet_retrieve = WalletViewSet.as_view({
	'get': 'retrieve'
})

urlpatterns = [
	url(r'^$', wallet_retrieve, name='wallet_retrieve'),
]
