# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings


class Notification(models.Model):
	RELATED_CHOICES = (
		('refer', 'Refer'),
		('official', 'Official Message'),
		('comment', 'Comment'),
		('wallet', 'Wallet'),
		('subscribe', 'Subscribe'),
		('company', 'Company'),
		('user', 'User'),
	)

	receiver = models.ForeignKey('accounts.AccountInfo', related_name='notifications', on_delete=models.CASCADE, default=settings.OFFICIAL_ACCOUNT_INFO_ID)
	sender = models.ForeignKey('accounts.AccountInfo', related_name='send_notifications', null=True, blank=True)

	content = models.CharField(max_length=200)
	related = models.CharField(max_length=200, null=True, blank=True, choices=RELATED_CHOICES)

	read = models.BooleanField(default=False)

	# Timestamp
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return self.content[:20]

	class Meta:
		ordering = ['-created']
