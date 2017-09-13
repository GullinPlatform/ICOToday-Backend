from rest_framework import serializers

from .models import Post, PostTag, RatingDetail
from ..accounts.serializers import BasicTeamSerializer, BasicAccountSerializer


class PostTagSerializer(serializers.ModelSerializer):
	class Meta:
		model = PostTag
		fields = ['tag']


class PostSerializer(serializers.ModelSerializer):
	tags = PostTagSerializer(required=False, allow_null=True, many=True, read_only=True)
	team = BasicTeamSerializer(required=False, allow_null=True, read_only=True)

	class Meta:
		model = Post
		exclude = ['marked']
		read_only_fields = ('created', 'updated', 'status')


class BasicPostSerializer(serializers.ModelSerializer):
	tags = PostTagSerializer(required=False, allow_null=True, many=True)
	team = BasicTeamSerializer(allow_null=True)

	class Meta:
		model = Post
		fields = ['id', 'team', 'description_short',
		          'logo_image', 'promote_image', 'title', 'type', 'category',
		          'status', 'tags', 'website', 'maximum_goal', 'minimum_goal', 'coin_type',
		          'start_datetime', 'end_datetime', 'current', 'money_raised', 'equality_on_offer',
		          'medium', 'twitter', 'slack', 'telegram']

		read_only_fields = ('created', 'updated', 'status')


class RatingDetailSerializer(serializers.ModelSerializer):
	rater = BasicAccountSerializer(read_only=True)

	class Meta:
		model = RatingDetail
		fields = ['rater', 'post', 'detail', 'created', 'updated', 'score']

		read_only_fields = ('created', 'updated')
