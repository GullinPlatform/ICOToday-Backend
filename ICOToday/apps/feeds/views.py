# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from ..projects.models import Project
from ..companies.models import Company
from .serializers import Feed, ReplySerializer, FeedSerializer

from ..accounts.views import send_email, AccountInfo


class FeedViewSet(viewsets.ViewSet):
	queryset = Feed.objects.all()
	parser_classes = (MultiPartParser, FormParser, JSONParser)
	permission_classes = (IsAuthenticatedOrReadOnly,)

	def my_feeds(self, request, page=None):
		import itertools
		from operator import attrgetter
		my_feeds_queryset = request.user.info.feeds.filter(reply_to=None)

		marked_project_feed = []
		following_user_feed = []

		for project in request.user.info.marked_projects.all():
			marked_project_feed = itertools.chain(marked_project_feed, project.company.feeds.all())

		for following in request.user.info.followings.all():
			following_user_feed = itertools.chain(marked_project_feed, following.feeds.all())

		result_list = sorted(set(itertools.chain(my_feeds_queryset, marked_project_feed, following_user_feed)),
		                     key=attrgetter('created'),
		                     reverse=True)
		paginator = Paginator(result_list, 10)

		try:
			feeds = paginator.page(page)
		except PageNotAnInteger:
			# If page is not an integer, deliver first page.
			feeds = paginator.page(1)
		except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
			feeds = paginator.page(paginator.num_pages)

		serializer = FeedSerializer(feeds, many=True)

		return Response(serializer.data, status=status.HTTP_200_OK)

	def company_feeds(self, request, company_id):
		company = get_object_or_404(Company.objects.all(), id=company_id)
		serializer = FeedSerializer(company.feeds.filter(reply_to=None), many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

	def user_feeds(self, request, account_info_id):
		account_info = get_object_or_404(AccountInfo.objects.all(), id=account_info_id)
		serializer = FeedSerializer(account_info.feeds.filter(reply_to=None), many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

	def create(self, request):
		company_id = request.data.get('company_id')
		if company_id:
			serializer = FeedSerializer(data=request.data, context={'creator_id': request.user.info.id, 'company_id': company_id})
			serializer.is_valid(raise_exception=True)
			serializer.save()

			# Send Email
			try:
				project = Company.objects.get(id=company_id).project
				email_list = []
				# TODO: email
				for marked in project.marked.all():
					email_list.append(marked.account.email)
				if request.user.info in project.company.members.all():
					send_email(email_list, 'ICOToday - Official Team Member Posted a Comment in ICO Project', 'NewComment', {id: project.id})
				else:
					send_email(email_list, 'ICOToday - New Comment on ICO You Subscribe to', 'NewComment', {id: project.id})
			except:  # RelatedObjectDoesNotExist could happen
				pass

		else:
			serializer = FeedSerializer(data=request.data, context={'creator_id': request.user.info.id})
			serializer.is_valid(raise_exception=True)
			serializer.save()

		return Response(serializer.data, status=status.HTTP_201_CREATED)

	def delete(self, request, feed_id):
		feed = get_object_or_404(self.queryset, id=feed_id)
		if feed.creator_id is request.user.info.id:
			feed.delete()
			return Response(status=status.HTTP_200_OK)
		else:
			return Response(status=status.HTTP_403_FORBIDDEN)

	def reply(self, request, feed_id):
		company_id = request.data.get('company_id')
		if company_id:
			serializer = ReplySerializer(data=request.data,
			                             context={'creator_id' : request.user.info.id,
			                                      'company_id' : company_id,
			                                      'reply_to_id': feed_id})
			serializer.is_valid(raise_exception=True)
			serializer.save()
		else:
			serializer = ReplySerializer(data=request.data,
			                             context={'creator_id' : request.user.info.id,
			                                      'reply_to_id': feed_id})
			serializer.is_valid(raise_exception=True)
			serializer.save()

		# TODO: send notification and email
		# feed = get_object_or_404(self.queryset, id=feed_id)
		# Send Email
		# send_email([feed.creator.account.email], 'ICOToday - New Reply on Your Comment', 'NewComment')

		return Response(serializer.data, status=status.HTTP_201_CREATED)
