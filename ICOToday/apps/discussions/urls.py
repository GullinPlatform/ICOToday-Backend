from django.conf.urls import url

from .views import CommentViewSet

comment = CommentViewSet.as_view({
	'get' : 'list',
	'post': 'create',
})

comment_reply = CommentViewSet.as_view({
	'post': 'reply',
})

comment_edit = CommentViewSet.as_view({
	'patch' : 'update',
	'delete': 'delete'
})

urlpatterns = [
	url(r'^(?P<post_pk>[0-9]+)/$', comment, name='comment'),

	url(r'^(?P<comment_pk>[0-9]+)/reply/$', comment_reply, name='comment_reply'),
	url(r'^(?P<comment_pk>[0-9]+)/edit/$', comment_edit, name='comment_edit'),
]
