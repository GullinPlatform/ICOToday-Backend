from django.utils import timezone, dateparse

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser, FileUploadParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Post, PostTag, RatingDetail

from .serializers import PostSerializer, PostTagSerializer, BasicPostSerializer, RatingDetailSerializer
from ..discussions.serializers import CommentSerializer


class PostViewSet(viewsets.ViewSet):
	queryset = Post.objects.all()
	parser_classes = (MultiPartParser, FormParser, JSONParser, FileUploadParser)
	permission_classes = (IsAuthenticatedOrReadOnly,)

	def list(self, request, p=None):
		queryset = self.queryset.filter(status=1)
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

	# TODO:
	def filtered_list(self, request):
		pass

	def create(self, request):
		Post.objects.create(
			creator_id=request.user.id,
			title=request.data.get('title'),
			description_full=request.data.get('description_full'),
			team_id=request.user.info.team.id,
			maximum_goal=request.data.get('maximum_goal'),
			minimum_goal=request.data.get('minimum_goal'),
			coin_type=request.data.get('coin_type'),
			start_datetime=request.data.get('start_datetime'),
			end_datetime=request.data.get('end_datetime'),
			logo_image=request.data.get('logo_image'),
			promote_image=request.data.get('promote_image', ''),
			white_paper=request.data.get('white_paper'),
			video_link=request.data.get('video_link', ''),
			website=request.data.get('website'),
			medium=request.data.get('medium'),
			twitter=request.data.get('twitter'),
			slack=request.data.get('slack'),
			telegram=request.data.get('telegram'),
		)
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
			serializer.save()
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
		post.marked.add(request.user)
		post.save()
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
				RatingDescription.objects.create(
					rater_id=request.user.id,
					description=request.data.get('descriptions'),
					post_id=post.id
				)
		else:
			return Response(status=status.HTTP_403_FORBIDDEN)
