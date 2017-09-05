from django.conf.urls import url

from .views import CommentViewSet

comment = CommentViewSet.as_view({
	'get'   : 'retrieve',
	'patch' : 'update',
	'delete': 'delete'
})

comment_create = CommentViewSet.as_view({
	'post': 'create',

})
comment_list = CommentViewSet.as_view({
	'get': 'list',
})

comment_reply = CommentViewSet.as_view({
	'post' : 'reply',
})

urlpatterns = [
	url(r'^$', comment_create, name='comment-create'),
	url(r'p/^(?P<post_pk>[0-9]+)/$', comment_list, name='comment-list'),
	url(r'^(?P<pk>[0-9]+)/$', comment, name='comment'),
	url(r'^(?P<pk>[0-9]+)/reply/$', comment_reply, name='comment-reply'),
]
