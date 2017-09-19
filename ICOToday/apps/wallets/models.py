# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Wallet(models.Model):
	btc_amount = models.FloatField(default=0.0)
	eth_amount = models.FloatField(default=0.0)
	icc_amount = models.FloatField(default=0.0)

	btc_wallet_address = models.CharField(max_length=50, blank=True, null=True)
	eth_wallet_address = models.CharField(max_length=50, blank=True, null=True)
	icc_wallet_address = models.CharField(max_length=50, blank=True, null=True)

	account = models.OneToOneField('accounts.Account', related_name='wallet')

	# Timestamp
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.account.email + ' Wallet'