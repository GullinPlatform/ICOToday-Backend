# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

from .views import AccountViewSet, AccountRegisterViewSet, ExpertApplicationViewSet

account_change_password = AccountViewSet.as_view({
	'post': 'change_password'
})

account_detail = AccountViewSet.as_view({
	'get'   : 'retrieve',
	'delete': 'destroy'
})

account_me = AccountViewSet.as_view({
	'get': 'me',
	'put': 'me'
})

account_register = AccountRegisterViewSet.as_view({
	'post': 'register'
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
	'post' : 'invite_email_resend',
})

account_forget_password = AccountRegisterViewSet.as_view({
	'get' : 'forget_password',  # Verify Token
	'post': 'forget_password',  # Get Token && Send email
	'put' : 'forget_password',  # Change Pass
})
#
# account_created_posts = AccountViewSet.as_view({
# 	'get': 'created_posts'
# })

account_marked_posts = AccountViewSet.as_view({
	'get': 'marked_posts'
})

account_two_factor = AccountViewSet.as_view({
	'post': 'two_factor_auth',
	'put' : 'two_factor_auth'
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
	# Account Detail
	url(r'^me/$', account_me, name='me'),
	url(r'^(?P<pk>[0-9]+)/$', account_detail, name='user-detail'),

	# Login Signup and verification email
	url(r'^signup/$', account_register, name='user-register'),
	url(r'^login/$', obtain_jwt_token),
	url(r'^check_login_status/$', verify_jwt_token),
	url(r'^refresh_login_status/$', refresh_jwt_token),
	url(r'^invited_signup/(?P<token>[A-z0-9\-]+)/$', account_invited_register, name='user-invited-register'),
	url(r'^invited_resend/(?P<token>[A-z0-9\-]+)/$', account_invite_email_resend, name='user-invited-resend-email'),
	url(r'^email_verify/$', account_verification, name='user-email-verify'),
	url(r'^email_verify/(?P<token>[A-z0-9\-]+)/$', account_verification, name='user-email-verify'),

	# Change Password
	url(r'^change_pass/$', account_change_password, name='user-change-pass'),

	url(r'^forget/$', account_forget_password, name='user-forget-password'),
	url(r'^forget/(?P<token>[A-z0-9\-]+)/$', account_forget_password, name='user-forget-password'),

	url(r'^2factor/$', account_two_factor, name='user-two-factor'),


	url(r'^me/marked_posts/$', account_marked_posts, name='me-marked-posts'),
	url(r'^(?P<pk>[0-9]+)/marked_posts/$', account_marked_posts, name='user-marked-posts'),

	url(r'^search/(?P<search_token>[A-z0-9\-]+)/$', account_search, name='user-search'),

	# url(r'^me/created_posts/$', account_created_posts, name='me-created-posts'),
	# url(r'^(?P<pk>[0-9]+)/created_posts/$', account_created_posts, name='user-created-posts'),

	# Expert Application
	url(r'^expert_apply/$', expert_application, name='expert-application'),
]
