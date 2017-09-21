# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

from .views import CompanyViewSet


company_list = CompanyViewSet.as_view({
	'get': 'list'
})

company_detail = CompanyViewSet.as_view({
	'get'   : 'retrieve',
	'post'  : 'create',
	'put'   : 'update',
	'patch' : 'add_team_member',
	'delete': 'add_team_member',
})


urlpatterns = [
	# Team
	url(r'$', company_list, name='company-list'),
	url(r'^new/$', company_detail, name='company-new'),
	url(r'^(?P<pk>[0-9]+)/$', company_detail, name='company-detail'),
]
