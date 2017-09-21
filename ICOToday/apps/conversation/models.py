# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Message(models.Model):
	# Relation
	conversation = models.ForeignKey('Conversation', related_name='messages')
	creator = models.ForeignKey('accounts.AccountInfo', related_name='messages')

	# Content
	content = models.TextField()
	read = models.BooleanField(default=False)

	# Timestamp
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return '%d to %d at %s' % self.sender_id, self.receiver_id, self.created.strftime('%B %d, %Y')

	class Meta:
		ordering = ['-created']


class Conversation(models.Model):
	users = models.ManyToManyField('accounts.AccountInfo', related_name='conversations')

	def __str__(self):
		return 'Conversation %d' % self.id
