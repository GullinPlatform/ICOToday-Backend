from rest_framework import serializers

from .models import Post, QuestionFile, QuestionField, QuestionTag


class QuestionFileSerializer(serializers.ModelSerializer):
	class Meta:
		model = QuestionFile
		fields = '__all__'


class QuestionFieldSerializer(serializers.ModelSerializer):
	class Meta:
		model = QuestionField
		fields = '__all__'


class QuestionTagSerializer(serializers.ModelSerializer):
	class Meta:
		model = QuestionTag
		fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
	files = QuestionFileSerializer(required=False, allow_null=True, many=True)
	fields = QuestionFieldSerializer(required=False, allow_null=True, many=True)
	industry_tags = QuestionTagSerializer(required=False, allow_null=True, many=True)
	tech_tags = QuestionTagSerializer(required=False, allow_null=True, many=True)

	class Meta:
		model = Post
		fields = '__all__'
		read_only_fields = ('created', 'updated', 'status')

