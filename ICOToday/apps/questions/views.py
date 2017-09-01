from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser, FileUploadParser
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from .models import Question, QuestionField, QuestionFile
from .serializers import QuestionSerializer

from ..discussions.serializers import DiscussionSerializer


class QuestionViewSet(viewsets.ViewSet):
	queryset = Question.objects.filter(status=1)
	parser_classes = (MultiPartParser, FormParser, JSONParser, FileUploadParser)
	permission_classes = (IsAuthenticatedOrReadOnly,)

	def list(self, request, p=None):
		paginator = Paginator(self.queryset, 10)
		try:
			questions = paginator.page(p)
		except PageNotAnInteger:
			# If page is not an integer, deliver first page.
			questions = paginator.page(1)
		except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
			questions = paginator.page(paginator.num_pages)

		serializer = QuestionSerializer(questions, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

	# TODO:
	def filtered_list(self, request):
		pass

	def created_question_list(self, request, pk):
		serializer = QuestionSerializer(request.user.created_questions, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

	def applied_question_list(self, request, pk):
		serializer = QuestionSerializer(request.user.applied_questions, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

	def marked_question_list(self, request, pk):
		serializer = QuestionSerializer(request.user.marked_questions, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

	def create(self, request):
		new_question = Question(
			creator_id=request.user.id,
			title=request.data['title'],
			description_short=request.data['description_short'],
			prize=request.data['prize']
		)
		new_question.save()

		for file in request.FILES.values():
			new_question_file = QuestionFile(file=file,
			                                 file_name=file.name,
			                                 file_size=file.size,
			                                 question_id=new_question.id)
			new_question_file.save()

		# 'industry_tags'
		# 'tech_tags'

		return Response(status=status.HTTP_201_CREATED)

	def retrieve(self, request, pk):
		question = get_object_or_404(self.queryset, pk=pk)
		serializer = QuestionSerializer(question)
		return Response(serializer.data, status=status.HTTP_200_OK)

	def update(self, request, pk):
		question = get_object_or_404(self.queryset, pk=pk)
		serializer = QuestionSerializer(question, data=request.data)

		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk):
		question = get_object_or_404(self.queryset, pk=pk)
		if request.user.is_staff or question.account_id == request.user.id:
			question.delete()
		else:
			return Response(status=status.HTTP_403_FORBIDDEN)

	def add_fields(self, request, pk):
		question = get_object_or_404(self.queryset, pk=pk)
		for field in request.data:
			question_field = QuestionField(title=field[0], description=field[1], question=question)
			question_field.save()
		return Response(status=status.HTTP_201_CREATED)

	def discussion_list(self, request, pk):
		question = get_object_or_404(Question.objects.all(), pk=pk)
		discussions = question.discussions
		serializer = DiscussionSerializer(discussions, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

	def apply_question(self, request, pk):
		question = get_object_or_404(self.queryset, pk=pk)
		question.appliers.add(request.user)
		question.save()
		return Response(status=status.HTTP_200_OK)

	def mark_question(self, request, pk):
		question = get_object_or_404(self.queryset, pk=pk)
		question.marked.add(request.user)
		question.save()
		return Response(status=status.HTTP_200_OK)
