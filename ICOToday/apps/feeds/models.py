# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Feed(models.Model):
	TYPE_CHOICES = (
		(0, 'User Feed'),
		(1, 'Company Post'),
		(2, 'User Comment on Company'),
		(3, 'Expert Review'),
		(4, 'Reply'),
	)
	type = models.IntegerField(choices=TYPE_CHOICES, default=0)

	# Feed Info
	creator = models.ForeignKey('accounts.AccountInfo', related_name='feeds')
	content = models.TextField()
	reply_to = models.ForeignKey('self', related_name='replies', null=True, blank=True, on_delete=models.CASCADE)

	# Relations
	# Notice: the company field here means the feed is by a company, if this field is null, then its a normal feed (personal feed)
	company = models.ForeignKey('companies.Company', related_name='feeds', null=True, blank=True)

	# Timestamp
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.content[:15]

	class Meta:
		ordering = ['-created']