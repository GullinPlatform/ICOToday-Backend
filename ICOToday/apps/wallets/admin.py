# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from ..accounts.models import AccountInfo
from ..companies.models import Company
from .models import Wallet


class AccountInfoInline(admin.TabularInline):
	model = AccountInfo
	fields = ('id', 'first_name', 'last_name', 'type', 'is_verified')
	readonly_fields = ('id', 'first_name', 'last_name', 'type', 'is_verified')
	show_change_link = True
	extra = 0


class CompanyInline(admin.TabularInline):
	model = Company
	fields = ('id', 'name', 'created')
	readonly_fields = ('id', 'name', 'created')
	show_change_link = True
	extra = 0


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
	list_display = ('id', 'account', 'company', 'ict_amount', 'created')
	fieldsets = [
		[None, {'fields': ['btc_amount', 'eth_amount', 'ict_amount']}],
		['Address', {'fields': ['btc_wallet_address', 'eth_wallet_address', 'ict_wallet_address']}],
		['Timestamp', {'fields': ['created', 'updated']}],
	]
	readonly_fields = ('created', 'updated', 'btc_amount', 'eth_amount', 'btc_wallet_address', 'eth_wallet_address')
	inlines = [AccountInfoInline, CompanyInline]


def token_stat():
	total = 0
	for wallet in Wallet.objects.all():
		total += wallet.ict_amount
	return u'%s' % total
