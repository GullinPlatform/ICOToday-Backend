# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from ..utils.upload_filename import company_icon_upload


class Company(models.Model):
	# Company Info
	name = models.CharField(max_length=50, null=True)
	description = models.TextField(null=True, blank=True)
	company_icon = models.ImageField(upload_to=company_icon_upload, null=True, blank=True)

	# Timestamp
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name


class PromotionApplication(models.Model):
	STATUS_CHOICES = (
		(0, 'Processing'),
		(1, 'Approved'),
		(2, 'Declined'),
	)

	# Info
	account = models.ForeignKey('accounts.AccountInfo', related_name='promotions')
	company = models.ForeignKey('companies.Company', related_name='promotions')
	detail = models.TextField()
	status = models.IntegerField(default=0, choices=STATUS_CHOICES)
	response = models.TextField()

	# Timestamp
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.team.name
