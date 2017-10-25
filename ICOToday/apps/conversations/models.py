# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Message(models.Model):
	"""
	Message Model
	Relations:
	field name | key type | origin model
	"""
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
		return unicode(self.id)

	class Meta:
		ordering = ['-created']


class Conversation(models.Model):
	"""
	Conversation Model
	Relations:
	field name | key type | origin model
	1) messages ForeignKey conversations.Message
	"""
	users = models.ManyToManyField('accounts.AccountInfo', related_name='conversations')

	def __str__(self):
		return 'Conversation %d' % self.id
