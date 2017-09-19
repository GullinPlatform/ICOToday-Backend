# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Notification(models.Model):
	RELATED_LINK_CHOICES = (
		('refer', 'Refer'),
		('official', 'Official Message'),
		('comment', 'Comment'),
		('refer', 'Refer'),
		('subscribe', 'Subscribe'),
	)

	receiver = models.ForeignKey('accounts.Account', related_name='notifications')
	sender = models.ForeignKey('accounts.Account', related_name='send_notifications', null=True, blank=True)

	content = models.CharField(max_length=200)
	related_link = models.CharField(max_length=200, null=True, blank=True, choices=RELATED_LINK_CHOICES)

	read = models.BooleanField(default=False)
	created = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.content
