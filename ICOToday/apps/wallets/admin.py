# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Wallet


class WalletAdmin(admin.ModelAdmin):
	list_display = ('id', 'account', 'ict_amount', 'created')
	fieldsets = [
		[None, {'fields': ['btc_amount', 'eth_amount', 'ict_amount']}],
		['Address', {'fields': ['btc_wallet_address', 'eth_wallet_address', 'ict_wallet_address']}],
		['Timestamp', {'fields': ['created', 'updated']}],
	]
	readonly_fields = ('created', 'updated', 'btc_amount', 'eth_amount', 'btc_wallet_address', 'eth_wallet_address')


admin.site.register(Wallet, WalletAdmin)
