# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from ..utils.upload_filename import company_icon_upload, company_certificate_upload


class Company(models.Model):
	# Company Info
	name = models.CharField(max_length=50, unique=True)
	icon = models.ImageField(upload_to=company_icon_upload)
	description = models.TextField()
	is_verified = models.BooleanField(default=False)

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


class CompanyVerification(models.Model):
	company = models.ForeignKey('Company', related_name='verification')
	certificate = models.FileField(upload_to=company_certificate_upload)

	# Timestamp
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.company.name + ' certificate'
