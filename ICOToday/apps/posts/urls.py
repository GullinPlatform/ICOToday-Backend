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

post_promo_list = PostViewSet.as_view({
	'get': 'promo_list',
})

post_close = PostViewSet.as_view({
	'get': 'close',
})

post_comments = PostViewSet.as_view({
	'get': 'comment_list'
})

post_mark = PostViewSet.as_view({
	'post': 'mark_post'
})

post_rating_detail = PostViewSet.as_view({
	'get': 'retrieve_rating_detail'
})

post_search = PostViewSet.as_view({
	'get': 'filtered_list'
})

search_posts_by_tag = PostViewSet.as_view({
	'get': 'search_by_tag'
})

get_post_tags = PostViewSet.as_view({
	'get': 'get_tag_list'
})

urlpatterns = [
	url(r'^$', post_list, name='post_list'),
	url(r'^p/(?P<p>[0-9]+)/$', post_list, name='post_list_page'),
	url(r'^promo/$', post_promo_list, name='post_promo_list'),
	url(r'^close/$', post_close, name='post_close'),
	url(r'^search/(?P<p>[0-9]+)/$', post_search, name='post_search'),

	url(r'^tags/$', get_post_tags, name='get_post_tags'),

	url(r'^(?P<pk>[0-9]+)/$', post, name='post'),
	url(r'^(?P<pk>[0-9]+)/rating/$', post_rating_detail, name='post-rating'),
	url(r'^(?P<pk>[0-9]+)/comments/$', post_comments, name='post-comments'),
	url(r'^(?P<pk>[0-9]+)/mark/$', post_mark, name='post_mark'),

]
