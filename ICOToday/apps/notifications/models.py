# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Notification(models.Model):
	RELATED_CHOICES = (
		('refer', 'Refer'),
		('official', 'Official Message'),
		('comment', 'Comment'),
		('wallet', 'Wallet'),
		('subscribe', 'Subscribe'),
	)

	receiver = models.ForeignKey('accounts.AccountInfo', related_name='notifications')
	sender = models.ForeignKey('accounts.AccountInfo', related_name='send_notifications', null=True, blank=True)

	content = models.CharField(max_length=200)
	related = models.CharField(max_length=200, null=True, blank=True, choices=RELATED_CHOICES)

	read = models.BooleanField(default=False)

	# Timestamp
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return self.content

	class Meta:
		ordering = ['-created']
