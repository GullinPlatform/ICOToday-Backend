# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from .models import Wallet


class WalletSerializer(serializers.ModelSerializer):
	class Meta:
		model = Wallet
		fields = ['btc_amount', 'eth_amount', 'ict_amount', 'btc_wallet_address', 'eth_wallet_address', 'ict_wallet_address', 'created', 'updated']
		read_only_fields = ('created', 'updated',)
