from rest_framework import serializers

from .models import Post, PostTag
from ..accounts.serializers import BasicAccountSerializer, BasicTeamSerializer


class PostTagSerializer(serializers.ModelSerializer):
	class Meta:
		model = PostTag
		fields = ['tag']


class PostSerializer(serializers.ModelSerializer):
	tags = PostTagSerializer(required=False, allow_null=True, many=True, read_only=True)
	team = BasicTeamSerializer(required=False, allow_null=True, read_only=True)

	class Meta:
		model = Post
		fields = '__all__'
		read_only_fields = ('created', 'updated', 'status')


class BasicPostSerializer(serializers.ModelSerializer):
	tags = PostTagSerializer(required=False, allow_null=True, many=True)
	team = BasicTeamSerializer(allow_null=True)

	class Meta:
		model = Post
		fields = ['id', 'team', 'description_short',
		          'logo_image', 'promote_image', 'title',
		          'status', 'tags', 'website', 'maximum_goal', 'minimum_goal', 'coin_type',
		          'start_datetime', 'end_datetime', 'current', 'money_raised',
		          'medium', 'twitter', 'slack', 'telegram']

		read_only_fields = ('created', 'updated', 'status')
