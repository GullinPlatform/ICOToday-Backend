# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from ..accounts.models import AccountInfo
from .models import Company, PromotionApplication, CompanyVerification


class CompanyMembersInline(admin.TabularInline):
	model = AccountInfo
	fields = ('id', 'first_name', 'last_name', 'title')
	readonly_fields = ('id', 'first_name', 'last_name', 'title')
	show_change_link = True
	extra = 0
	fk_name = "company"
	verbose_name = "Company Member"
	verbose_name_plural = "Company Members"


class CompanyAdminsInline(admin.TabularInline):
	model = AccountInfo
	fields = ('id', 'first_name', 'last_name', 'title')
	readonly_fields = ('id', 'first_name', 'last_name', 'title')
	show_change_link = True
	extra = 0
	fk_name = "company"
	verbose_name = "Company Admin"
	verbose_name_plural = "Company Admins"


class CompanyAdmin(admin.ModelAdmin):
	list_display = ('name', 'description', 'is_verified', 'created')
	fieldsets = [
		[None, {'fields': ['name', 'icon', 'description', 'is_verified']}],
		['Timestamp', {'fields': ['created', 'updated']}],
	]
	readonly_fields = ('created', 'updated')
	inlines = [CompanyMembersInline, CompanyAdminsInline]


class PromotionApplicationAdmin(admin.ModelAdmin):
	list_display = ('company', 'status', 'created')
	fieldsets = [
		[None, {'fields': ['company', 'account', 'detail', 'response']}],
		['Status', {'fields': ['status']}],

		['Timestamp', {'fields': ['created', 'updated']}],
	]
	readonly_fields = ('created', 'updated')


class CompanyVerificationAdmin(admin.ModelAdmin):
	list_display = ('id', 'company', 'created')
	fieldsets = [
		[None, {'fields': ['company', 'account', 'detail', 'response']}],
		['Status', {'fields': ['status']}],

		['Timestamp', {'fields': ['created', 'updated']}],
	]
	readonly_fields = ('created', 'updated')


admin.site.register(Company, CompanyAdmin)
admin.site.register(PromotionApplication, PromotionApplicationAdmin)
