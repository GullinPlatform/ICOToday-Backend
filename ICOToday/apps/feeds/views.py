# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticated

from ..projects.models import Project
from .models import Feed
from .serializers import ReplySerializer, FeedSerializer
from ..accounts.views import send_email


class FeedViewSet(viewsets.ViewSet):
	queryset = Feed.objects.all()
	parser_classes = (MultiPartParser, FormParser, JSONParser)
	permission_classes = (IsAuthenticated,)

	def list(self, request, project_id):
		post = get_object_or_404(Project.objects.all(), id=project_id)
		serializer = FeedSerializer(post.comments.filter(reply_to=None), many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

	def create(self, request, project_id):
		serializer = FeedSerializer(data=request.data, context={'creator_id': request.user.info.id, 'project_id': project_id})
		serializer.is_valid(raise_exception=True)
		serializer.save()

		# Send Email
		project = Project.objects.get(id=project_id)

		email_list = []
		for marked in project.marked.all():
			email_list.append(marked.email)
		if request.user.info in project.team.members.all():
			send_email(email_list, 'ICOToday - Official Team Member Posted a Comment in ICO Project', 'NewComment', {id: project_id})
		else:
			send_email(email_list, 'ICOToday - New Comment on ICO You Subscribe to', 'NewComment', {id: project_id})

		return Response(serializer.data, status=status.HTTP_201_CREATED)

	def update(self, request, comment_id):
		comment = get_object_or_404(self.queryset, id=comment_id)
		if request.data.get('content', None) and comment.creator_id is request.user.info.id:
			serializer = FeedSerializer(comment, data=request.data, partial=True)
			serializer.is_valid(raise_exception=True)
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			return Response(status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, comment_id):
		comment = get_object_or_404(self.queryset, id=comment_id)
		if comment.creator_id is request.user.info.id:
			comment.delete()
			return Response(status=status.HTTP_200_OK)
		else:
			return Response(status=status.HTTP_403_FORBIDDEN)

	def reply(self, request, comment_id):
		comment = get_object_or_404(self.queryset, id=comment_id)

		serializer = ReplySerializer(data=request.data,
		                             context={'creator_id' : request.user.info.id,
		                                      'post_id'    : comment.post_id,
		                                      'reply_to_id': comment_id})
		serializer.is_valid(raise_exception=True)
		serializer.save()

		# Send Email
		send_email([comment.creator.email], 'ICOToday - New Reply on Your Comment', 'NewComment', {id: comment.post_id})

		return Response(serializer.data, status=status.HTTP_201_CREATED)
