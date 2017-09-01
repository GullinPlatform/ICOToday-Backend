from rest_framework import serializers

from .models import Post, PostTag, CommentsField
from ..accounts.serializers import BasicAccountSerializer, BasicTeamSerializer


class CommentsFieldSerializer(serializers.ModelSerializer):
	class Meta:
		model = CommentsField
		fields = '__all__'


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
	team = BasicTeamSerializer(allow_null=True)

	class Meta:
		model = Post
		fields = ['id', 'team', 'description_short', 'logo_image', 'promote_image', 'title', 'status', 'tags', 'website', 'start_datetime', 'end_datetime']
		read_only_fields = ('created', 'updated', 'status')
