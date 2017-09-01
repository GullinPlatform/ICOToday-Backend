from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

from .views import AccountViewSet, AccountRegisterViewSet, TeamSerializer

account_change_password = AccountViewSet.as_view({
	'post': 'change_password'
})

account_detail = AccountViewSet.as_view({
	'get'   : 'retrieve',
	'delete': 'destroy'
})

account_me = AccountViewSet.as_view({
	'get': 'me'
})

account_register = AccountRegisterViewSet.as_view({
	'post': 'register'
})

account_register_token = AccountRegisterViewSet.as_view({
	'post': 'send_token',
	'put' : 'verify_token'
})

account_forget_password = AccountRegisterViewSet.as_view({
	'post': 'forget_password'
})

account_verify_info = AccountViewSet.as_view({
	'post': 'verify_info'
})

team_list = TeamSerializer.as_view({
	'get': 'retrieve'
})

team_detail = TeamSerializer.as_view({
	'post': 'create',
	'get' : 'list'
})

urlpatterns = [
	# Account
	url(r'^(?P<pk>[0-9]+)/$', account_detail, name='user-detail'),
	# url(r'^avatar/$', account_avatar, name='user-avatar'),
	url(r'^login/$', obtain_jwt_token),
	url(r'^reset/$', account_change_password, name='change-pass'),
	url(r'^signup/$', account_register, name='user-register'),
	url(r'^token/$', account_register_token, name='user-token'),
	url(r'^refresh/$', refresh_jwt_token),
	url(r'^forget/(?P<token>[A-z0-9\-]+)/$', account_forget_password, name='user-forget-password'),
	url(r'^me/$', account_me, name='me'),
	url(r'^me/verify/$', account_verify_info),
	url(r'^verify/$', verify_jwt_token),

	# Team
	url(r'^teams/$', team_list,  name='team-list'),
	url(r'^team/new/$', team_detail, name='team-list'),
	url(r'^team/(?P<pk>[0-9]+)/$', team_detail, name='team-list'),

]
