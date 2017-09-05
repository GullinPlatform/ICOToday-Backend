#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models


class Comment(models.Model):
	post = models.ForeignKey('posts.Post', related_name='comments')
	account = models.ForeignKey('accounts.Account', related_name='replies')
	content = models.TextField()
	reply_to = models.ForeignKey('self', related_name='replies', null=True, blank=True)
	# Timestamp
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.question.title


class Message(models.Model):
	sender = models.ForeignKey('accounts.Account', related_name='send_messages')
	receiver = models.ForeignKey('accounts.Account', related_name='received_messages')
	content = models.TextField()
	# Timestamp
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return '%d to %d at %s' % self.sender_id, self.receiver_id, self.created.strftime('%B %d, %Y')
