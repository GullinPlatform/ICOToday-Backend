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

urlpatterns = [
	url(r'^$', question_list, name='question_list'),
	url(r'^p/(?P<p>[0-9]+)$', question_list, name='question_list'),

	url(r'^applied/$', applied_question_list, name='applied_question_list'),
	url(r'^marked/$', marked_question_list, name='marked_question_list'),
	url(r'^created/$', created_question_list, name='created_question_list'),

	url(r'^(?P<pk>[0-9]+)/$', question, name='question'),
	url(r'^(?P<pk>[0-9]+)/discussions/$', question_discussions, name='question'),
	url(r'^(?P<pk>[0-9]+)/apply/$', question_apply, name='question_apply'),
	url(r'^(?P<pk>[0-9]+)/mark/$', question_mark, name='question_mark'),

]
