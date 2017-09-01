from rest_framework import serializers

from .models import Post, QuestionFile, QuestionField, PostTag


class QuestionFileSerializer(serializers.ModelSerializer):
	class Meta:
		model = QuestionFile
		fields = '__all__'


class QuestionFieldSerializer(serializers.ModelSerializer):
	class Meta:
		model = QuestionField
		fields = '__all__'


class PostTagSerializer(serializers.ModelSerializer):
	class Meta:
		model = PostTag
		fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
	files = QuestionFileSerializer(required=False, allow_null=True, many=True)
	fields = QuestionFieldSerializer(required=False, allow_null=True, many=True)
	tags = PostTagSerializer(required=False, allow_null=True, many=True)

	class Meta:
		model = Post
		fields = '__all__'
		read_only_fields = ('created', 'updated', 'status')

