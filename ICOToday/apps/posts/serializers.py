from rest_framework import serializers

from .models import Post, PostTag
from ..accounts.serializers import BasicAccountSerializer


class PostTagSerializer(serializers.ModelSerializer):
	class Meta:
		model = PostTag
		fields = ['tag']


class PostSerializer(serializers.ModelSerializer):
	tags = PostTagSerializer(required=False, allow_null=True, many=True)
	team_members = BasicAccountSerializer(required=False, allow_null=True, many=True)

	class Meta:
		model = Post
		fields = '__all__'
		read_only_fields = ('created', 'updated', 'status')


class BasicPostSerializer(serializers.ModelSerializer):
	tags = PostTagSerializer(required=False, allow_null=True, many=True)

	class Meta:
		model = Post
		fields = ['id', 'description_short', 'logo_image', 'promo_image', 'title', 'status', 'tags', 'website', 'start_date', 'end_date']
		read_only_fields = ('created', 'updated', 'status')
