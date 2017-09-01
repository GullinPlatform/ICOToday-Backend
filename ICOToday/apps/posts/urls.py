from django.conf.urls import url

from .views import QuestionViewSet

question = QuestionViewSet.as_view({
	'get'   : 'retrieve',
	'patch' : 'update',
	'delete': 'delete'
})

question_list = QuestionViewSet.as_view({
	'get' : 'list',
	'post': 'create'
})

question_discussions = QuestionViewSet.as_view({
	'get': 'discussion_list'
})

question_apply = QuestionViewSet.as_view({
	'post': 'apply_question'
})

question_mark = QuestionViewSet.as_view({
	'post': 'mark_question'
})

created_question_list = QuestionViewSet.as_view({
	'post': 'created_question_list'
})

applied_question_list = QuestionViewSet.as_view({
	'post': 'applied_question_list'
})

marked_question_list = QuestionViewSet.as_view({
	'post': 'marked_question_list'
})

add_team_member = QuestionViewSet.as_view({
	'post': 'add_team_member',
	'delete': 'add_team_member'
})

search_posts_by_tag = QuestionViewSet.as_view({
	'get': 'search_by_tag'
})

get_post_tags = QuestionViewSet.as_view({
	'get': 'get_tag_list'
})

urlpatterns = [
	url(r'^$', question_list, name='question_list'),
	url(r'^p/(?P<p>[0-9]+)$', question_list, name='question_list'),

	url(r'^applied/$', applied_question_list, name='applied_question_list'),
	url(r'^marked/$', marked_question_list, name='marked_question_list'),
	url(r'^created/$', created_question_list, name='created_question_list'),

	url(r'^search/t/(?P<tag>[A-z0-9]+)/$', search_posts_by_tag, name='search_posts_by_tag'),
	url(r'^tags/$', get_post_tags, name='get_post_tags'),

	url(r'^(?P<pk>[0-9]+)/$', question, name='question'),
	url(r'^(?P<pk>[0-9]+)/discussions/$', question_discussions, name='question'),
	url(r'^(?P<pk>[0-9]+)/apply/$', question_apply, name='question_apply'),
	url(r'^(?P<pk>[0-9]+)/mark/$', question_mark, name='question_mark'),
	url(r'^(?P<pk>[0-9]+)/add_team_member/$', add_team_member, name='add_team_member'),


]
