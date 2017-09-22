# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser, FileUploadParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Project, ProjectTag

from .serializers import ProjectSerializer, ProjectTagSerializer, BasicProjectSerializer
from ..feeds.serializers import FeedSerializer

from ..utils.send_email import send_email


class ProjectViewSet(viewsets.ViewSet):
	queryset = Project.objects.all()
	parser_classes = (MultiPartParser, FormParser, JSONParser, FileUploadParser)
	permission_classes = (IsAuthenticatedOrReadOnly,)

	def list(self, request, p=None):
		queryset = self.queryset.exclude(status=0)
		paginator = Paginator(queryset, 10)
		try:
			projects = paginator.page(p)
		except PageNotAnInteger:
			# If page is not an integer, deliver first page.
			projects = paginator.page(1)
		except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
			projects = paginator.page(paginator.num_pages)

		serializer = BasicProjectSerializer(projects, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

	def promo_list(self, request):
		queryset = self.queryset.filter(status=3)
		serializer = BasicProjectSerializer(queryset, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

	# TODO: Link URL
	def statistic(self, request):
		query = self.queryset.exclude(status=0)
		now = timezone.now()
		active = query.filter(start_datetime__lte=now, end_datetime__gte=now).count()
		upcoming = query.filter(start_datetime__gte=now).count()
		passed = query.filter(end_datetime__lte=now).count()

		return Response({'active': active, 'upcoming': upcoming, 'passed': passed})

	def close(self, request):
		for project in self.queryset:
			if project.time_passed():
				project.status = 4
				project.save()
		return Response(status=status.HTTP_200_OK)

	def search(self, request, p=None):
		query = self.queryset.exclude(status=0)
		# Cache query in memory to improve performance
		[q for q in query]
		# First filter by status
		if request.GET.get('status'):
			project_status = request.GET.get('status')
			now = timezone.now()
			if project_status == 'active':
				query = query.filter(start_datetime__lte=now, end_datetime__gte=now)
			if project_status == 'upcoming':
				query = query.filter(start_datetime__gte=now)
			if project_status == 'passed':
				query = query.filter(end_datetime__lte=now)
		# Then filter by category
		if request.GET.get('category'):
			query = query.filter(category=request.GET.get('category'))
		# Then filter by type
		if request.GET.get('type'):
			query = query.filter(type=type)
		# Then search by keyword
		if request.GET.get('keyword'):
			for project in query:
				if request.GET.get('keyword').lower() not in project.title.lower():
					query = query.exclude(id=project.id)
		# Then paginate
		paginator = Paginator(query, 10)
		try:
			projects = paginator.page(p)
		except PageNotAnInteger:
			# If page is not an integer, deliver first page.
			projects = paginator.page(1)
		except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
			projects = paginator.page(paginator.num_pages)

		serializer = BasicProjectSerializer(projects, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

	def create(self, request):
		if request.user.type != 0 or not request.user.is_verified:
			return Response(status=status.HTTP_403_FORBIDDEN)

		form = request.data
		for key in form:
			if form[key] == '' or form[key] == 'null':
				form[key] = None

		project = Project.objects.create(
			creator_id=request.user.id,
			team_id=request.user.info.team.id,

			title=form.get('title'),
			logo_image=form.get('logo_image'),
			category=form.get('category'),
			description_full=form.get('description_full'),
			description_short=form.get('description_short'),
			type=form.get('type'),

			maximum_goal=form.get('maximum_goal', None),
			minimum_goal=form.get('minimum_goal', None),
			equality_on_offer=form.get('equality_on_offer', None),
			coin_unit=form.get('coin_unit', None),
			coin_name=form.get('coin_name', None),
			ratio=form.get('ratio', None),
			accept=form.get('accept', None),
			start_datetime=form.get('start_datetime', None),
			end_datetime=form.get('end_datetime', None),
			promote_image=form.get('promote_image', None),
			white_paper=form.get('white_paper', None),
			video_link=form.get('video_link', None),
			website=form.get('website', None),
			medium=form.get('medium', None),
			twitter=form.get('twitter', None),
			slack=form.get('slack', None),
			telegram=form.get('telegram', None),
		)
		# Subscribe for project creator
		for member in request.user.info.team.members.all():
			try:
				project.marked.add(member.account.info)
			except:
				pass
		return Response(status=status.HTTP_201_CREATED)

	def retrieve(self, request, id):
		project = get_object_or_404(self.queryset, id=id)
		serializer = ProjectSerializer(project)
		return Response(serializer.data, status=status.HTTP_200_OK)

	def retrieve_rating_detail(self, request, id):
		pass

	# TODO:
	# project = get_object_or_404(self.queryset, id=id)
	# serializer = RatingDetailSerializer(project.rating_detail, many=True)
	# return Response(serializer.data, status=status.HTTP_200_OK)

	def update(self, request, id):
		project = get_object_or_404(self.queryset, id=id)
		serializer = ProjectSerializer(project, data=request.data, partial=True)
		if serializer.is_valid():
			project = serializer.save()

			# Bulk send update emails
			email_list = []
			for marked in project.marked.all():
				email_list.append(marked.account.email)
			send_email(email_list, 'ICOToday - Official Update on ICO Project You Subscribe to', 'ProjectUpdate', {id: project.id})
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, id):
		project = get_object_or_404(self.queryset, id=id)
		if project.id == request.user.info.company_admin.id:
			project.delete()
		else:
			return Response(status=status.HTTP_403_FORBIDDEN)

	def comment_list(self, request, id):
		project = get_object_or_404(Project.objects.all(), id=id)
		discussions = project.discussions
		serializer = FeedSerializer(discussions, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

	def mark_project(self, request, id):
		project = get_object_or_404(self.queryset, id=id)
		if request.user.info in project.marked.all():
			project.marked.remove(request.user.info)
		else:
			project.marked.add(request.user.info)
		return Response(status=status.HTTP_200_OK)

	def search_by_tag(self, request, tag):
		tag = ProjectTag.objects.get(tag=tag)
		if tag:
			serializer = ProjectSerializer(tag.projects.all(), many=True)
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			return Response(status=status.HTTP_404_NOT_FOUND)

	# TODO:
	def rate(self, request, id):
		pass

	# 	# Is Expert
	# 	if request.user.type == 3:
	# 		project = get_object_or_404(self.queryset, id=id)
	# 		if request.data.get('descriptions', False):
	# 			RatingDetail.objects.create(
	# 				rater_id=request.user.id,
	# 				description=request.data.get('descriptions'),
	# 				project_id=project.id
	# 			)
	# 	else:
	# 		return Response(status=status.HTTP_403_FORBIDDEN)


class ProjectTagViewSet(viewsets.ViewSet):
	queryset = ProjectTag.objects.all()
	parser_classes = (MultiPartParser, FormParser, JSONParser)
	permission_classes = (IsAuthenticatedOrReadOnly,)

	def list(self, request):
		serializer = ProjectTagSerializer(self.queryset, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)
