from django.conf.urls import url

from .views import DiscussionViewSet

discussion = DiscussionViewSet.as_view({
	'get'   : 'retrieve',
	'patch' : 'update',
	'delete': 'delete'
})

discussion_create = DiscussionViewSet.as_view({
	'post': 'create',
})

discussion_reply = DiscussionViewSet.as_view({
	'post': 'reply',
	'patch': 'update_reply',

})

urlpatterns = [
	url(r'^$', discussion_create, name='discussion-create'),
	url(r'^(?P<pk>[0-9]+)/$', discussion, name='discussion'),
	url(r'^(?P<pk>[0-9]+)/reply/$', discussion_reply, name='discussion-reply'),
]
