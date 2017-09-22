# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from ..rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

from .views import AccountViewSet, AccountRegisterViewSet, ExpertApplicationViewSet

account_change_password = AccountViewSet.as_view({
	'post': 'change_password'
})

account_detail = AccountViewSet.as_view({
	'get'   : 'retrieve'
})

account_me = AccountViewSet.as_view({
	'get': 'me',
	'put': 'me'
})

account_register = AccountRegisterViewSet.as_view({
	'post': 'register'
})

account_logout = AccountRegisterViewSet.as_view({
	'post': 'logout'
})

account_invited_register = AccountRegisterViewSet.as_view({
	'get' : 'invited_register',
	'post': 'invited_register'
})

account_verification = AccountRegisterViewSet.as_view({
	'get' : 'email_verify',  # Verify Token
	'post': 'email_verify',  # Resend Email
})

account_invite_email_resend = AccountRegisterViewSet.as_view({
	'post': 'invite_email_resend',
})

account_forget_password = AccountRegisterViewSet.as_view({
	'get' : 'forget_password',  # Verify Token
	'post': 'forget_password',  # Get Token && Send email
	'put' : 'forget_password',  # Change Pass
})

account_marked_projects = AccountViewSet.as_view({
	'get': 'marked_projects'
})

account_two_factor = AccountViewSet.as_view({
	'post': 'two_factor_auth',  # Send Email
	'get' : 'two_factor_auth'  # Verify Token
})

account_search = AccountViewSet.as_view({
	'get': 'search'
})

expert_application = ExpertApplicationViewSet.as_view({
	'get' : 'retrieve',
	'post': 'create',
	'put' : 'update',
})

urlpatterns = [
	# Login Signup and Stay Login
	url(r'^login/$', obtain_jwt_token),
	url(r'^signup/$', account_register, name='user-register'),
	url(r'^logout/$', account_logout, name='user-logout'),
	url(r'^refresh_login_status/$', refresh_jwt_token),

	# Account Detail
	url(r'^me/$', account_me, name='me'),
	url(r'^(?P<pk>[0-9]+)/$', account_detail, name='user-detail'),

	#  Verification email
	url(r'^invited_signup/(?P<token>[A-z0-9\-]+)/$', account_invited_register, name='user-invited-register'),
	url(r'^invited_resend/(?P<token>[A-z0-9\-]+)/$', account_invite_email_resend, name='user-invited-resend-email'),
	url(r'^email_verify/$', account_verification, name='user-email-verify'),
	url(r'^email_verify/(?P<token>[A-z0-9\-]+)/$', account_verification, name='user-email-verify'),

	# Change Password
	url(r'^change_pass/$', account_change_password, name='user-change-pass'),
	url(r'^forget/$', account_forget_password, name='user-forget-password'),
	url(r'^forget/(?P<token>[A-z0-9\-]+)/$', account_forget_password, name='user-forget-password'),

	# 2 Factor Authentication
	url(r'^2factor/$', account_two_factor, name='user-two-factor'),

	# Marked Project
	url(r'^me/marked_projects/$', account_marked_projects, name='me-marked-projects'),
	url(r'^(?P<pk>[0-9]+)/marked_projects/$', account_marked_projects, name='user-marked-projects'),

	# Search User
	url(r'^search/(?P<search_token>[A-z0-9\-]+)/$', account_search, name='user-search'),

	# Expert Application
	url(r'^expert_apply/$', expert_application, name='expert-application'),
]
