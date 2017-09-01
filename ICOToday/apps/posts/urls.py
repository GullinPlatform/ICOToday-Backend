from django.conf.urls import url

from .views import PostViewSet

post = PostViewSet.as_view({
	'get'   : 'retrieve',
	'patch' : 'update',
	'delete': 'delete'
})

post_list = PostViewSet.as_view({
	'get' : 'list',
	'post': 'create'
})

post_discussions = PostViewSet.as_view({
	'get': 'discussion_list'
})

post_apply = PostViewSet.as_view({
	'post': 'apply_post'
})

post_mark = PostViewSet.as_view({
	'post': 'mark_post'
})

created_post_list = PostViewSet.as_view({
	'post': 'created_post_list'
})

applied_post_list = PostViewSet.as_view({
	'post': 'applied_post_list'
})

marked_post_list = PostViewSet.as_view({
	'post': 'marked_post_list'
})

add_team_member = PostViewSet.as_view({
	'post': 'add_team_member',
	'delete': 'add_team_member'
})

search_posts_by_tag = PostViewSet.as_view({
	'get': 'search_by_tag'
})

get_post_tags = PostViewSet.as_view({
	'get': 'get_tag_list'
})

urlpatterns = [
	url(r'^$', post_list, name='post_list'),
	url(r'^p/(?P<p>[0-9]+)$', post_list, name='post_list'),

	url(r'^applied/$', applied_post_list, name='applied_post_list'),
	url(r'^marked/$', marked_post_list, name='marked_post_list'),
	url(r'^created/$', created_post_list, name='created_post_list'),

	url(r'^search/t/(?P<tag>[A-z0-9]+)/$', search_posts_by_tag, name='search_posts_by_tag'),
	url(r'^tags/$', get_post_tags, name='get_post_tags'),

	url(r'^(?P<pk>[0-9]+)/$', post, name='post'),
	url(r'^(?P<pk>[0-9]+)/discussions/$', post_discussions, name='post'),
	url(r'^(?P<pk>[0-9]+)/apply/$', post_apply, name='post_apply'),
	url(r'^(?P<pk>[0-9]+)/mark/$', post_mark, name='post_mark'),
	url(r'^(?P<pk>[0-9]+)/add_team_member/$', add_team_member, name='add_team_member'),


]
