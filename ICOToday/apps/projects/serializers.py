from rest_framework import serializers

from .models import Project, ProjectTag, PromotionApplication


from ..companies.serializers import BasicCompanySerializer


class ProjectTagSerializer(serializers.ModelSerializer):
	class Meta:
		model = ProjectTag
		fields = ['tag']


class ProjectSerializer(serializers.ModelSerializer):
	tags = ProjectTagSerializer(required=False, allow_null=True, many=True, read_only=True)
	team = BasicCompanySerializer(required=False, allow_null=True, read_only=True)

	class Meta:
		model = Project
		exclude = ['marked']
		read_only_fields = ('created', 'updated', 'status')


class BasicProjectSerializer(serializers.ModelSerializer):
	tags = ProjectTagSerializer(required=False, allow_null=True, many=True)
	team = BasicCompanySerializer(allow_null=True)

	class Meta:
		model = Project
		fields = ['id', 'company', 'description_short',
		          'logo_image', 'promote_image', 'title', 'type', 'category',
		          'status', 'tags', 'website', 'maximum_goal', 'minimum_goal', 'coin_unit','accept',
		          'start_datetime', 'end_datetime', 'current', 'money_raised', 'equality_on_offer',
		          'medium', 'twitter', 'slack', 'telegram']

		read_only_fields = ('created', 'updated', 'status')


class PromotionApplicationSerializer(serializers.ModelSerializer):
	class Meta:
		model = PromotionApplication
		fields = '__all__'
		read_only_fields = ('created', 'updated')
