# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group as AdminGroup

from .forms import AccountChangeForm, AccountCreationForm
from .models import Account, AccountInfo, VerifyToken, ExpertApplication


class AccountInline(admin.TabularInline):
	model = Account
	fields = ('id', 'email', 'phone')
	readonly_fields = ('id', 'email', 'phone')
	show_change_link = True
	extra = 0


class AccountInfoInline(admin.TabularInline):
	model = AccountInfo
	fields = ('id', 'first_name', 'last_name', 'title', 'company', 'is_advisor')
	readonly_fields = ('id', 'first_name', 'last_name', 'title', 'company', 'is_advisor')
	show_change_link = True
	extra = 0


class AccountAdmin(UserAdmin):
	# The forms to add and change user instances
	form = AccountChangeForm
	add_form = AccountCreationForm
	list_display = ('id', 'email', 'phone', 'created', 'updated')
	list_filter = ['is_staff', 'created']
	fieldsets = (
		(None, {'fields': ('email', 'phone', 'password', 'info', 'is_staff')}),
		('Timestamp', {'fields': ('created', 'updated')})
	)
	readonly_fields = ('created', 'updated', 'is_staff',)
	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields' : ('email', 'password1', 'password2')}
		 ),
	)
	search_fields = ['email']
	ordering = ['email', ]


class AccountInfoAdmin(admin.ModelAdmin):
	list_display = ('id', 'first_name', 'last_name', 'type', 'is_verified', 'updated', 'last_login_ip')
	fieldsets = (
		('Personal Info', {'fields': ('avatar', 'first_name', 'last_name', 'type', 'title', 'description', 'interests')}),
		('Verify Status', {'fields': ('is_verified',)}),
		('Company Info', {'fields': ('company', 'company_admin', 'company_pending')}),
		('Social Media', {'fields': ('linkedin', 'twitter', 'facebook', 'telegram')}),
		('Security', {'fields': ('last_login_ip',)}),
		('Timestamp', {'fields': ('created', 'updated')})
	)
	list_filter = ['type', 'is_verified', 'company_admin']
	search_fields = ['first_name', 'last_name']
	readonly_fields = ('created', 'updated', 'last_login_ip')
	inlines = [AccountInline]


class VerifyTokenAdmin(admin.ModelAdmin):
	list_display = ('account', 'is_expired')
	fieldsets = (
		(None, {'fields': ('account', 'token', 'expire_time', 'is_expired')}),
	)
	list_filter = ['expire_time']
	readonly_fields = ('is_expired', 'expire_time')


class ExpertApplicationAdmin(admin.ModelAdmin):
	list_display = ('account', 'status', 'created')
	fieldsets = (
		(None, {'fields': ['account', 'detail', 'status', 'response']}),
		('Timestamp', {'fields': ['created', 'updated']}),
	)
	list_filter = ['status', 'created', ]

	readonly_fields = ('created', 'updated')


admin.site.register(Account, AccountAdmin)
admin.site.register(AccountInfo, AccountInfoAdmin)
admin.site.register(VerifyToken, VerifyTokenAdmin)
admin.site.register(ExpertApplication, ExpertApplicationAdmin)
admin.site.unregister(AdminGroup)
