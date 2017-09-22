# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

from .views import ProjectViewSet, ProjectTagViewSet

project = ProjectViewSet.as_view({
	'get'   : 'retrieve',
	'patch' : 'update',
	'delete': 'delete'
})

project_list = ProjectViewSet.as_view({
	'get' : 'list',
	'post': 'create'
})

project_promo_list = ProjectViewSet.as_view({
	'get': 'promo_list',
})

project_close = ProjectViewSet.as_view({
	'get': 'close',
})

project_comments = ProjectViewSet.as_view({
	'get': 'comment_list'
})

project_mark = ProjectViewSet.as_view({
	'post': 'mark_project'
})

project_rating_detail = ProjectViewSet.as_view({
	'get': 'retrieve_rating_detail'
})

project_search = ProjectViewSet.as_view({
	'get': 'search'
})

search_projects_by_tag = ProjectViewSet.as_view({
	'get': 'search_by_tag'
})

all_tags = ProjectTagViewSet.as_view({
	'get': 'list'
})

urlpatterns = [
	url(r'^$', project_list, name='project_list'),
	url(r'^p/(?P<p>[0-9]+)/$', project_list, name='project_list_page'),
	url(r'^promo/$', project_promo_list, name='project_promo_list'),
	url(r'^close/$', project_close, name='project_close'),
	url(r'^search/(?P<p>[0-9]+)/$', project_search, name='project_search'),


	url(r'^(?P<id>[0-9]+)/$', project, name='project'),
	url(r'^(?P<id>[0-9]+)/rating/$', project_rating_detail, name='project-rating'),
	url(r'^(?P<id>[0-9]+)/comments/$', project_comments, name='project-comments'),
	url(r'^(?P<id>[0-9]+)/mark/$', project_mark, name='project_mark'),

	url(r'^tags/$', all_tags, name='project_tags'),

]
