# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Wallet(models.Model):
	"""
	Wallet Model
	Relations:
	field name | key type | origin model
	1) account OneToOneField accounts.AccountInfo
	2) company OneToOneField companies.Company
	"""
	btc_amount = models.FloatField(default=0.0)
	eth_amount = models.FloatField(default=0.0)
	ict_amount = models.FloatField(default=0.0)

	btc_wallet_address = models.CharField(max_length=50, blank=True, null=True)
	eth_wallet_address = models.CharField(max_length=50, blank=True, null=True)
	ict_wallet_address = models.CharField(max_length=50, blank=True, null=True)

	# Timestamp
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
