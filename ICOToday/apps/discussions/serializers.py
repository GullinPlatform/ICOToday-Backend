from rest_framework import serializers

from .models import Comment, Message

from ..accounts.serializers import BasicAccountSerializer


class ReplySerializer(serializers.ModelSerializer):
	creator = BasicAccountSerializer(read_only=True)

	class Meta:
		model = Comment
		fields = ['id', 'post_id', 'creator', 'content', 'created', 'updated', 'reply_to_id']
		read_only_fields = ('created', 'updated')

	def create(self, validated_data):
		validated_data['creator_id'] = self.context['creator_id']
		validated_data['post_id'] = self.context['post_id']
		validated_data['reply_to_id'] = self.context['reply_to_id']
		return Comment.objects.create(**validated_data)


class CommentSerializer(serializers.ModelSerializer):
	creator = BasicAccountSerializer(read_only=True)
	replies = ReplySerializer(many=True, required=False, read_only=True)

	class Meta:
		model = Comment
		fields = ['id', 'post_id', 'creator', 'content', 'created', 'updated', 'replies']
		read_only_fields = ('created', 'updated')

	def create(self, validated_data):
		validated_data['creator_id'] = self.context['creator_id']
		validated_data['post_id'] = self.context['post_id']
		return Comment.objects.create(**validated_data)
