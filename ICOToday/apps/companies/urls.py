# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

from .views import CompanyViewSet

company_create = CompanyViewSet.as_view({
	'post': 'create',
})

company_detail = CompanyViewSet.as_view({
	'get': 'retrieve',
	'put': 'update',
})

company_member_list = CompanyViewSet.as_view({
	'get': 'members',
})

company_member_manage = CompanyViewSet.as_view({
	'post'  : 'member_manage',
	'delete': 'member_manage',
})

company_member_apply = CompanyViewSet.as_view({
	'post': 'apply',
})

company_member_leave = CompanyViewSet.as_view({
	'delete': 'leave',
})

company_admin_list = CompanyViewSet.as_view({
	'get': 'admins',
})

company_admin_manage = CompanyViewSet.as_view({
	'post': 'admin_manage',
})

company_member_application_manage = CompanyViewSet.as_view({
	'post'  : 'member_application',
	'delete': 'member_application',
})

company_search = CompanyViewSet.as_view({
	'get': 'search',
})

urlpatterns = [
	# Company list and create
	url(r'^$', company_create, name='company-create'),
	url(r'^(?P<company_id>[0-9]+)/$', company_detail, name='company-detail'),
	url(r'^(?P<company_id>[0-9]+)/members/$', company_member_list, name='company-member-list'),
	url(r'^(?P<company_id>[0-9]+)/apply/$', company_member_apply, name='company-member-apply'),
	url(r'^leave/$', company_member_leave, name='company-member-leave'),
	url(r'^admins/$', company_admin_list, name='company-admin-list'),

	url(r'^member/$', company_member_manage, name='company-member-create'),
	url(r'^member/(?P<account_info_id>[0-9]+)/$', company_member_manage, name='company-member-add-delete'),
	url(r'^member/approve/(?P<account_info_id>[0-9]+)/$', company_member_application_manage, name='company-member-approve-reject'),
	url(r'^member/admin/(?P<account_info_id>[0-9]+)/$', company_admin_manage, name='company-add-admin'),

	url(r'^search/$', company_search, name='company-search'),
]
