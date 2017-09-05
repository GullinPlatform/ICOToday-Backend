from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticated, AllowAny

from ..posts.models import Post
from .models import Comment
from .serializers import ReplySerializer, CommentSerializer


class CommentViewSet(viewsets.ViewSet):
	queryset = Comment.objects.all()
	parser_classes = (MultiPartParser, FormParser, JSONParser)
	permission_classes = (IsAuthenticated,)

	def list(self, request, post_pk):
		post = get_object_or_404(Post.objects.all(), pk=post_pk)
		serializer = CommentSerializer(post.comments, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

	def create(self, request):
		serializer = CommentSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return Response(status=status.HTTP_201_CREATED)

	def retrieve(self, request, pk):
		discussion = get_object_or_404(self.queryset, pk=pk)
		serializer = CommentSerializer(discussion)
		return Response(serializer.data, status=status.HTTP_200_OK)

	def update(self, request, pk):
		question = get_object_or_404(self.queryset, pk=pk)
		serializer = CommentSerializer(question, data=request.data)

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

	def reply(self, request, pk):
		comment = get_object_or_404(self.queryset, pk=pk)
		serializer = ReplySerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return Response(status=status.HTTP_201_CREATED)
