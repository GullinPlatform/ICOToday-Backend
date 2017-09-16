from django.utils import timezone, dateparse
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser, FileUploadParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Post, PostTag, RatingDetail

from .serializers import PostSerializer, PostTagSerializer, BasicPostSerializer, RatingDetailSerializer
from ..discussions.serializers import CommentSerializer
from ..accounts.views import send_email


class PostViewSet(viewsets.ViewSet):
	queryset = Post.objects.all()
	parser_classes = (MultiPartParser, FormParser, JSONParser, FileUploadParser)
	permission_classes = (IsAuthenticatedOrReadOnly,)

	def list(self, request, p=None):
		queryset = self.queryset.exclude(status=0)
		paginator = Paginator(queryset, 10)
		try:
			posts = paginator.page(p)
		except PageNotAnInteger:
			# If page is not an integer, deliver first page.
			posts = paginator.page(1)
		except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
			posts = paginator.page(paginator.num_pages)

		serializer = BasicPostSerializer(posts, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

	def promo_list(self, request):
		queryset = self.queryset.filter(status=3)
		serializer = BasicPostSerializer(queryset, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

	def close(self, request):
		for post in self.queryset:
			if post.time_passed():
				post.status = 4
				post.save()
		return Response(status=status.HTTP_200_OK)

	def filtered_list(self, request, p=None):
		query = self.queryset.exclude(status=0)
		# First filter by status
		if request.GET.get('status'):
			post_status = request.GET.get('status')
			now = timezone.now()
			if post_status == 'active':
				query = query.filter(start_datetime__lte=now, end_datetime__gte=now)
			if post_status == 'upcoming':
				query = query.filter(start_datetime__gte=now)
			if post_status == 'passed':
				query = query.filter(end_datetime__lte=now)
		# Then filter by category
		if request.GET.get('category'):
			query = query.filter(category=request.GET.get('category'))
		# Then filter by type
		if request.GET.get('type'):
			query = query.filter(type=type)
		# Then search by keyword
		if request.GET.get('keyword'):
			for post in query:
				if request.GET.get('keyword').lower() not in post.title.lower():
					query = query.exclude(id=post.id)
		# Then paginate
		paginator = Paginator(query, 10)
		try:
			posts = paginator.page(p)
		except PageNotAnInteger:
			# If page is not an integer, deliver first page.
			posts = paginator.page(1)
		except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
			posts = paginator.page(paginator.num_pages)

		serializer = BasicPostSerializer(posts, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

	def create(self, request):
		if request.user.type != 0 or not request.user.is_verified:
			return Response(status=status.HTTP_403_FORBIDDEN)

		form = request.data
		for key in form:
			if form[key] == '' or form[key] == 'null':
				form[key] = None

		post = Post.objects.create(
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
			coin_type=form.get('coin_type', None),
			coin_name=form.get('coin_name', None),
			ratio=form.get('ratio', None),
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
		# Subscribe for post creator
		for member in request.user.info.team.members.all():
			try:
				post.marked.add(member.account)
			except:
				pass
		return Response(status=status.HTTP_201_CREATED)

	def retrieve(self, request, pk):
		post = get_object_or_404(self.queryset, pk=pk)
		serializer = PostSerializer(post)
		return Response(serializer.data, status=status.HTTP_200_OK)

	def retrieve_rating_detail(self, request, pk):
		post = get_object_or_404(self.queryset, pk=pk)
		serializer = RatingDetailSerializer(post.rating_detail, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

	def update(self, request, pk):
		post = get_object_or_404(self.queryset, pk=pk)
		serializer = PostSerializer(post, data=request.data, partial=True)
		if serializer.is_valid():
			post = serializer.save()

			email_list = []
			for marked in post.marked.all():
				email_list.append(marked.email)

			send_email(email_list, 'ICOToday - Official Update on ICO Project You Subscribe to', 'NewComment', {id: post.id})
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk):
		post = get_object_or_404(self.queryset, pk=pk)
		if request.user.is_staff or post.account_id == request.user.id:
			post.delete()
		else:
			return Response(status=status.HTTP_403_FORBIDDEN)

	def comment_list(self, request, pk):
		post = get_object_or_404(Post.objects.all(), pk=pk)
		discussions = post.discussions
		serializer = CommentSerializer(discussions, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

	def mark_post(self, request, pk):
		post = get_object_or_404(self.queryset, pk=pk)
		if request.user in post.marked.all():
			post.marked.remove(request.user)
		else:
			post.marked.add(request.user)
		return Response(status=status.HTTP_200_OK)

	def search_by_tag(self, request, tag):
		tag = PostTag.objects.get(tag=tag)
		if tag:
			serializer = PostSerializer(tag.posts.all(), many=True)
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			return Response(status=status.HTTP_404_NOT_FOUND)

	def get_tag_list(self, request):
		tags = PostTag.objects.all()
		serializer = PostTagSerializer(tags, many=True)

		return Response(serializer.data, status=status.HTTP_200_OK)

	def rate(self, request, pk):
		# Is Expert
		if request.user.type == 3:
			post = get_object_or_404(self.queryset, pk=pk)
			if request.data.get('descriptions', False):
				RatingDetail.objects.create(
					rater_id=request.user.id,
					description=request.data.get('descriptions'),
					post_id=post.id
				)
		else:
			return Response(status=status.HTTP_403_FORBIDDEN)
