# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Company(models.Model):
	"""
	Company Model
	Relations:
	field name | key type | origin model
	1) members ForeignKey accounts.AccountInfo
    2) admins ForeignKey accounts.AccountInfo
	3) pending_members ForeignKey accounts.AccountInfo
	4) promotion_applications ForeignKey companies.PromotionApplication
	5) feeds ForeignKey feeds.Feed
	6) project OneToOneField projects.Project
	"""
	# Company Info
	name = models.CharField(max_length=50, unique=True)

	# Wallet
	wallet = models.OneToOneField('wallets.Wallet', related_name='company')

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
	company = models.ForeignKey('companies.Company', related_name='promotion_applications', on_delete=models.CASCADE)
	duration = models.IntegerField(default=1)  # Unit: days
	detail = models.TextField(null=True, blank=True)
	status = models.IntegerField(default=0, choices=STATUS_CHOICES)
	response = models.TextField(null=True, blank=True)
	eth_wallet_address = models.TextField(null=True, blank=True)

	# Timestamp
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.company.name

	class Meta:
		ordering = ['-created']
