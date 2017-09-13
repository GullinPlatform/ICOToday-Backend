from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticated, AllowAny

from ..posts.models import Post
from .models import Comment
from .serializers import ReplySerializer, CommentSerializer
from ..accounts.views import send_email


class CommentViewSet(viewsets.ViewSet):
	queryset = Comment.objects.all()
	parser_classes = (MultiPartParser, FormParser, JSONParser)
	permission_classes = (IsAuthenticated,)

	def list(self, request, post_pk):
		post = get_object_or_404(Post.objects.all(), pk=post_pk)
		serializer = CommentSerializer(post.comments.filter(reply_to=None), many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

	def create(self, request, post_pk):

		serializer = CommentSerializer(data=request.data, context={'creator_id': request.user.id, 'post_id': post_pk})
		serializer.is_valid(raise_exception=True)
		serializer.save()

		# Send Email
		post = Post.objects.get(pk=post_pk)

		email_list = []
		for marked in post.marked.all():
			email_list.append(marked.email)
		if request.user in post.team.members.all():
			send_email(email_list, 'ICOToday - Official Team Member Posted a Comment in ICO Project', 'NewComment', {id: post_pk})
		else:
			send_email(email_list, 'ICOToday - New Comment on ICO You Subscribe to', 'NewComment', {id: post_pk})

		return Response(serializer.data, status=status.HTTP_201_CREATED)

	def update(self, request, comment_pk):
		comment = get_object_or_404(self.queryset, pk=comment_pk)
		if request.data.get('content', None) and comment.creator_id is request.user.id:
			serializer = CommentSerializer(comment, data=request.data, partial=True)
			serializer.is_valid(raise_exception=True)
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			return Response(status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, comment_pk):
		comment = get_object_or_404(self.queryset, pk=comment_pk)
		if comment.creator_id is request.user.id:
			comment.delete()
			return Response(status=status.HTTP_200_OK)
		else:
			return Response(status=status.HTTP_403_FORBIDDEN)

	def reply(self, request, comment_pk):
		comment = get_object_or_404(self.queryset, pk=comment_pk)

		serializer = ReplySerializer(data=request.data,
		                             context={'creator_id' : request.user.id,
		                                      'post_id'    : comment.post_id,
		                                      'reply_to_id': comment_pk})
		serializer.is_valid(raise_exception=True)
		serializer.save()

		# Send Email
		send_email([comment.creator.email], 'ICOToday - New Reply on Your Comment', 'NewComment', {id: comment.post_id})

		return Response(serializer.data, status=status.HTTP_201_CREATED)
