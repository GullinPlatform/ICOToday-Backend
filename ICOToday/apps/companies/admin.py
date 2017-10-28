# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from ..accounts.models import AccountInfo
from ..feeds.models import Feed
from ..projects.models import Project

from .models import Company, PromotionApplication


class FeedInline(admin.TabularInline):
	model = Feed
	show_change_link = True
	extra = 1


class ProjectInline(admin.TabularInline):
	model = Project
	show_change_link = True
	fields = ('id', 'name', 'description_short', 'type', 'status')
	extra = 0


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


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
	list_display = ('name', 'created')
	fieldsets = [
		[None, {'fields': ['name']}],
		['Timestamp', {'fields': ['created', 'updated']}],
	]
	readonly_fields = ('created', 'updated')
	inlines = [ProjectInline, CompanyMembersInline, CompanyAdminsInline, FeedInline]


@admin.register(PromotionApplication)
class PromotionApplicationAdmin(admin.ModelAdmin):
	list_display = ('company', 'status', 'created')
	fieldsets = [
		[None, {'fields': ['company', 'account', 'detail', 'response']}],
		['Status', {'fields': ['status']}],

		['Timestamp', {'fields': ['created', 'updated']}],
	]
	readonly_fields = ('created', 'updated')
