# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core import urlresolvers

from django.utils.safestring import mark_safe
from django.contrib import admin

from .forms import AccountChangeForm, AccountCreationForm
from .models import Account, AccountInfo, VerifyToken, ExpertApplication

from django.contrib.auth.models import Group as AdminGroup

admin.site.unregister(AdminGroup)


class AccountInline(admin.TabularInline):
	model = Account
	fields = ('id', 'email', 'phone')
	readonly_fields = ('id', 'email', 'phone')
	show_change_link = True
	extra = 0


class AccountInfoInline(admin.TabularInline):
	model = AccountInfo
	fields = ('id', 'first_name', 'last_name', 'title', 'company')
	readonly_fields = ('id', 'first_name', 'last_name', 'title', 'company')
	show_change_link = True
	extra = 0


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
	# The forms to add and change user instances
	form = AccountChangeForm
	add_form = AccountCreationForm
	list_display = ('id', 'email', 'phone', 'created', 'updated')
	search_fields = ['email', 'phone']
	list_filter = ['is_staff', 'created']

	fieldsets = (
		(None, {'fields': ('email', 'phone', 'password', 'account_info', 'is_staff')}),
		('Timestamp', {'fields': ('created', 'updated')})
	)
	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields' : ('email', 'password1', 'password2')}
		 ),
	)
	readonly_fields = ('created', 'updated', 'is_staff', 'account_info')

	def account_info(self, obj):
		change_url = urlresolvers.reverse('admin:accounts_accountinfo_change', args=(obj.info.id,))
		account_info_instance = AccountInfo.objects.get(id=obj.info.id)
		return mark_safe('<a href="%s">%s</a>' % (change_url, account_info_instance))


@admin.register(AccountInfo)
class AccountInfoAdmin(admin.ModelAdmin):
	list_display = ('id', 'first_name', 'last_name', 'type', 'is_verified', 'whitelist', 'amount_to_invest', 'updated', 'last_login_ip')
	fieldsets = (
		('Personal Info', {'fields': ('avatar', 'first_name', 'last_name', 'type', 'title', 'description', 'interests')}),
		('Wallet', {'fields': ('user_wallet',)}),
		('Verify Status', {'fields': ('is_verified',)}),
		('Company Info', {'fields': ('company', 'company_admin', 'company_pending')}),
		('Social Media', {'fields': ('linkedin', 'twitter', 'facebook', 'telegram')}),
		('Security', {'fields': ('last_login_ip',)}),
		('White List', {'fields': ('whitelist', 'amount_to_invest')}),
		('Timestamp', {'fields': ('created', 'updated')})
	)
	list_filter = ['type', 'is_verified', 'company']
	search_fields = ['first_name', 'last_name']
	readonly_fields = ('created', 'updated', 'last_login_ip', 'user_wallet')
	inlines = [AccountInline]

	def user_wallet(self, obj):
		change_url = urlresolvers.reverse('admin:wallets_wallet_change', args=(obj.wallet.id,))
		return mark_safe('<a href="%s">%s</a>' % (change_url, 'Change'))

	def is_company_admin(self, obj):
		if obj.company_admin:
			return mark_safe('<img src="/static/admin/img/icon-yes.svg" alt="True">')
		else:
			return mark_safe('<img src="/static/admin/img/icon-no.svg" alt="False">')


@admin.register(VerifyToken)
class VerifyTokenAdmin(admin.ModelAdmin):
	list_display = ('account', 'is_expired')
	fieldsets = (
		(None, {'fields': ('account_info', 'token', 'expire_time', 'is_expired')}),
	)
	list_filter = ['expire_time']
	readonly_fields = ('is_expired', 'expire_time')

	def account_info(self, obj):
		change_url = urlresolvers.reverse('admin:accounts_accountinfo_change', args=(obj.account.id,))
		account_info_instance = AccountInfo.objects.get(id=obj.account.id)
		return mark_safe('<a href="%s">%s</a>' % (change_url, account_info_instance))


@admin.register(ExpertApplication)
class ExpertApplicationAdmin(admin.ModelAdmin):
	list_display = ('account', 'status', 'created')
	fieldsets = (
		('Account', {'fields': ['account_info']}),
		('Content', {'fields': ['detail', 'resume', 'previous_rating_example', 'status']}),
		('Timestamp', {'fields': ['created', 'updated']}),
	)
	list_filter = ['status', 'created', ]

	readonly_fields = ('created', 'updated', 'account_info')

	def account_info(self, obj):
		change_url = urlresolvers.reverse('admin:accounts_accountinfo_change', args=(obj.account.id,))
		account_info_instance = AccountInfo.objects.get(id=obj.account.id)
		return mark_safe('<a href="%s">%s</a>' % (change_url, account_info_instance))
