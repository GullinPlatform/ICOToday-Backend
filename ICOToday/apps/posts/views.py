from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser, FileUploadParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Post, PostTag
from ..accounts.models import Account

from .serializers import PostSerializer, PostTagSerializer, BasicPostSerializer
from ..discussions.serializers import DiscussionSerializer


class PostViewSet(viewsets.ViewSet):
	queryset = Post.objects.filter(status=1)
	parser_classes = (MultiPartParser, FormParser, JSONParser, FileUploadParser)
	permission_classes = (IsAuthenticatedOrReadOnly,)

	def list(self, request, p=None):
		paginator = Paginator(self.queryset, 10)
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

	# TODO:
	def filtered_list(self, request):
		pass

	def created_post_list(self, request, pk):
		serializer = PostSerializer(request.user.created_posts, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

	def applied_post_list(self, request, pk):
		serializer = PostSerializer(request.user.applied_posts, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

	def marked_post_list(self, request, pk):
		serializer = PostSerializer(request.user.marked_posts, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

	def create(self, request):
		new_post = Post(
			creator_id=request.user.id,
			title=request.data['title'],
			description_short=request.data['description_short'],
			prize=request.data['prize']
		)
		new_post.save()

		# for file in request.FILES.values():
		# 	new_post_file = PostFile(file=file,
		# 	                                 file_name=file.name,
		# 	                                 file_size=file.size,
		# 	                                 post_id=new_post.id)
		# 	new_post_file.save()

		# 'industry_tags'
		# 'tech_tags'

		return Response(status=status.HTTP_201_CREATED)

	def retrieve(self, request, pk):
		post = get_object_or_404(self.queryset, pk=pk)
		serializer = PostSerializer(post)
		return Response(serializer.data, status=status.HTTP_200_OK)

	def update(self, request, pk):
		post = get_object_or_404(self.queryset, pk=pk)
		serializer = PostSerializer(post, data=request.data)

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

	# def add_fields(self, request, pk):
	# 	post = get_object_or_404(self.queryset, pk=pk)
	# 	for field in request.data:
	# 		post_field = PostField(title=field[0], description=field[1], post=post)
	# 		post_field.save()
	# 	return Response(status=status.HTTP_201_CREATED)

	def discussion_list(self, request, pk):
		post = get_object_or_404(Post.objects.all(), pk=pk)
		discussions = post.discussions
		serializer = DiscussionSerializer(discussions, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

	def apply_post(self, request, pk):
		post = get_object_or_404(self.queryset, pk=pk)
		post.appliers.add(request.user)
		post.save()
		return Response(status=status.HTTP_200_OK)

	def mark_post(self, request, pk):
		post = get_object_or_404(self.queryset, pk=pk)
		post.marked.add(request.user)
		post.save()
		return Response(status=status.HTTP_200_OK)

	def add_team_member(self, request, pk):
		post = get_object_or_404(self.queryset, pk=pk)
		if request.method == 'POST':
			if request.data.get('member_id'):
				member = get_object_or_404(Account.objects.all(), id=int(request.data.get('member_id')))
				post.add(member)
				post.save()
				return Response(status=status.HTTP_200_OK)
			else:
				return Response(status=status.HTTP_400_BAD_REQUEST)

		elif request.method == 'DELETE':
			post.remove(request.user)
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
