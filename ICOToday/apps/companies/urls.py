# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

from .views import CompanyViewSet


company_list = CompanyViewSet.as_view({
	'get': 'list',
	'post': 'create',
})

company_detail = CompanyViewSet.as_view({
	'get'   : 'retrieve',
	'put'   : 'update',
})

company_member_manage = CompanyViewSet.as_view({
	'post' : 'member_manage',
	'delete': 'member_manage',
})

company_member_apply = CompanyViewSet.as_view({
	'post' : 'apply',
})

company_member_leave = CompanyViewSet.as_view({
	'delete': 'leave',
})

company_member_admin = CompanyViewSet.as_view({
	'post': 'add_company_admin',
})

company_member_application_manage = CompanyViewSet.as_view({
	'post': 'member_application',
	'delete': 'member_application',
})

company_search = CompanyViewSet.as_view({
	'get': 'search',
})

urlpatterns = [
	# Company list and create
	url(r'^$', company_list, name='company-list'),
	url(r'^(?P<company_id>[0-9]+)/$', company_detail, name='company-detail'),
	url(r'^(?P<company_id>[0-9]+)/members/$', company_detail, name='company-detail'),
	url(r'^(?P<company_id>[0-9]+)/apply/$', company_member_apply, name='company-member-apply'),
	url(r'^leave/$', company_member_leave, name='company-member-leave'),

	url(r'^member/$', company_member_manage, name='company-member-create'),
	url(r'^member/(?P<account_info_id>[0-9]+)/$', company_member_manage, name='company-member-add-delete'),
	url(r'^member/approve/(?P<account_info_id>[0-9]+)/$', company_member_application_manage, name='company-member-approve-reject'),
	url(r'^member/admin/(?P<account_info_id>[0-9]+)/$', company_member_admin, name='company-add-admin'),

	url(r'^search/$', company_search, name='company-search'),
]
