# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser, FileUploadParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Project, ProjectTag, ProjectRatingDetail
from ..accounts.serializers import AccountInfo, BasicAccountInfoSerializer

from .serializers import ProjectSerializer, ProjectTagSerializer, BasicProjectSerializer, ProjectRatingDetailSerializer

from ..utils.send_email import send_email


class ProjectViewSet(viewsets.ViewSet):
	queryset = Project.objects.all()
	parser_classes = (MultiPartParser, FormParser, JSONParser, FileUploadParser)
	permission_classes = (IsAuthenticatedOrReadOnly,)

	def promo_list(self, request):
		queryset = self.queryset.filter(status=3)
		serializer = BasicProjectSerializer(queryset, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

	def unrated_list(self, request):
		queryset = self.queryset.filter(rating=None)[:20]
		serializer = BasicProjectSerializer(queryset, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

	def user_rated_list(self, request, account_info_id):
		account_info = get_object_or_404(AccountInfo.objects.all(), id=account_info_id)
		queryset = self.queryset.filter(rating_details__rater=account_info)
		serializer = BasicProjectSerializer(queryset, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

	def statistic(self, request):
		query = self.queryset.exclude(status=0)
		now = timezone.now()
		active = query.filter(start_datetime__lte=now, end_datetime__gte=now).count()
		upcoming = query.filter(start_datetime__gte=now).count()
		passed = query.filter(end_datetime__lte=now).count()
		all = query.count()

		return Response({'active': active, 'upcoming': upcoming, 'passed': passed, 'all': all}, status=status.HTTP_200_OK)

	def close(self, request):
		for project in self.queryset:
			if project.time_passed():
				project.status = 4
				project.save()
		return Response(status=status.HTTP_200_OK)

	def search(self, request):
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
				if request.GET.get('keyword').lower() not in project.name.lower():
					query = query.exclude(id=project.id)
		# Then paginate
		paginator = Paginator(query, 10)
		p = request.GET.get('page')
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
		if request.user.info.type != 0 or not request.user.info.is_verified:
			return Response(status=status.HTTP_403_FORBIDDEN)

		form = request.data.copy()
		for key in form:
			if form[key] == '' or form[key] == 'null':
				form[key] = None

		project = Project.objects.create(
			company_id=request.user.info.company.id,

			name=request.user.info.company.name,
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
		for member in request.user.info.company.members.all():
			try:
				project.marked.add(member.account.info)
			except:
				pass
		return Response(status=status.HTTP_201_CREATED)

	def retrieve(self, request, project_id):
		project = get_object_or_404(self.queryset, id=project_id)
		serializer = ProjectSerializer(project)
		return Response(serializer.data, status=status.HTTP_200_OK)

	def update(self, request, project_id):
		project = get_object_or_404(self.queryset, id=project_id)
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

	def delete(self, request, project_id):
		project = get_object_or_404(self.queryset, id=project_id)
		if project.id == request.user.info.company_admin.id:
			project.delete()
		else:
			return Response(status=status.HTTP_403_FORBIDDEN)

	def mark_project(self, request, project_id):
		project = get_object_or_404(self.queryset, id=project_id)
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

	def subscribers(self, request, project_id):
		project = get_object_or_404(self.queryset, id=project_id)
		serializer = BasicAccountInfoSerializer(project.marked, many=True)

		return Response(serializer.data, status=status.HTTP_200_OK)


class ProjectTagViewSet(viewsets.ViewSet):
	queryset = ProjectTag.objects.all()
	parser_classes = (MultiPartParser, FormParser, JSONParser)
	permission_classes = (IsAuthenticatedOrReadOnly,)

	def list(self, request):
		serializer = ProjectTagSerializer(self.queryset, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)


class ProjectRatingDetailViewSet(viewsets.ViewSet):
	parser_classes = (MultiPartParser, FormParser, JSONParser)
	permission_classes = (IsAuthenticatedOrReadOnly,)

	def list(self, request, project_id):
		queryset = ProjectRatingDetail.objects.filter(project_id=project_id)
		serializer = ProjectRatingDetailSerializer(queryset, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

	def rate(self, request, project_id):
		# Return if user is nor expert
		if not request.user.info.type == 2:
			return Response(status=status.HTTP_403_FORBIDDEN)

		project = Project.objects.filter(id=project_id).first()
		if not project:
			return Response(status=status.HTTP_404_NOT_FOUND)

		if request.method == 'POST':
			count = ProjectRatingDetail.objects.filter(project_id=project_id, rater_id=request.user.info.id).count()
			if count > 0:
				return Response({'detail': 'user can only rate a project once'}, status=status.HTTP_400_BAD_REQUEST)

			# Create project rating
			project_rating = ProjectRatingDetail.objects.create(
				project_id=project_id,
				rater_id=request.user.info.id,
				score=request.data.get('score'),
				content=request.data.get('content'),
				file=request.data.get('file')
			)

			if project.rating:
				count = ProjectRatingDetail.objects.filter(project_id=project_id).count()
				project.rating = (int(project.rating) * count + int(request.data.get('score'))) / (count + 1)
				project.save()
			else:
				project.rating = int(request.data.get('score'))
				project.save()

			# TODO: Notification and email here
			serializer = ProjectRatingDetailSerializer(project_rating)
			return Response(serializer.data, status=status.HTTP_201_CREATED)

		elif request.method == 'PUT':
			project_rating = ProjectRatingDetail.objects.filter(project_id=project_id, rater_id=request.user.info.id).first()
			if not project_rating:
				return Response(status=status.HTTP_404_NOT_FOUND)

			project_rating.score = request.data.get('score')
			project_rating.content = request.data.get('content')
			project_rating.save()

			# TODO: Notification and email here
			serializer = ProjectRatingDetailSerializer(project_rating)
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		# No delete supported because they can review and delete to affect the score
