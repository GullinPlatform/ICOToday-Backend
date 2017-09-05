from rest_framework import serializers

from .models import Comment, Message


class ReplySerializer(serializers.ModelSerializer):
	class Meta:
		model = Comment
		fields = '__all__'
		read_only_fields = ('created', 'updated')


class CommentSerializer(serializers.ModelSerializer):
	replies = ReplySerializer(many=True, required=False)

	class Meta:
		model = Comment
		fields = '__all__'
		read_only_fields = ('created', 'updated')
