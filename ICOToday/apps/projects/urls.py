# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

from .views import ProjectViewSet, ProjectTagViewSet, ProjectRatingDetailViewSet

project = ProjectViewSet.as_view({
	'get'   : 'retrieve',
	'patch' : 'update',
	'delete': 'delete'
})

project_create = ProjectViewSet.as_view({
	'post': 'create'
})

project_stat = ProjectViewSet.as_view({
	'get': 'statistic',
})

project_promo_list = ProjectViewSet.as_view({
	'get': 'promo_list',
})

project_unrated_list = ProjectViewSet.as_view({
	'get': 'unrated_list',
})

project_user_rated_list = ProjectViewSet.as_view({
	'get': 'user_rated_list',
})

project_close = ProjectViewSet.as_view({
	'get': 'close',
})

project_mark = ProjectViewSet.as_view({
	'post': 'mark_project'
})

project_search = ProjectViewSet.as_view({
	'get': 'search'
})

project_subscribers = ProjectViewSet.as_view({
	'get': 'subscribers'
})

search_projects_by_tag = ProjectViewSet.as_view({
	'get': 'search_by_tag'
})

all_tags = ProjectTagViewSet.as_view({
	'get': 'list'
})

project_rating_detail_list = ProjectRatingDetailViewSet.as_view({
	'get': 'list'
})

project_rating_detail_rate = ProjectRatingDetailViewSet.as_view({
	'post': 'rate',
	'put' : 'rate'
})

project_rating_detail_retrieve = ProjectRatingDetailViewSet.as_view({
	'get': 'retrieve',
})

urlpatterns = [
	url(r'^$', project_create, name='project_create'),

	url(r'^stat/$', project_stat, name='project_stat'),
	url(r'^search/$', project_search, name='project_search'),
	url(r'^promo/$', project_promo_list, name='project_promo_list'),
	url(r'^close/$', project_close, name='project_close'),
	url(r'^unrated/$', project_unrated_list, name='project_unrated_list'),
	url(r'^rated/(?P<account_info_id>[0-9]+)/$', project_user_rated_list, name='project_user_rated_list'),

	url(r'^(?P<project_id>[0-9]+)/$', project, name='project'),
	url(r'^(?P<project_id>[0-9]+)/mark/$', project_mark, name='project_mark'),

	url(r'^tags/$', all_tags, name='project_tags'),

	url(r'^(?P<project_id>[0-9]+)/rating/$', project_rating_detail_list, name='project-rating'),
	url(r'^(?P<project_id>[0-9]+)/rate/$', project_rating_detail_rate, name='project-rate'),
	url(r'^(?P<project_id>[0-9]+)/subs/$', project_subscribers, name='project-subscribers'),

	url(r'^rt/(?P<project_rating_detail_id>[0-9]+)/$', project_rating_detail_retrieve, name='project_rating_detail_retrieve'),

]
