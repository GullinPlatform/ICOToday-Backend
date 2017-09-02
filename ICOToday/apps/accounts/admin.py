from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group as AdminGroup

from .forms import AccountChangeForm, AccountCreationForm
from .models import Account, AccountInfo, VerifyToken, Team


class AccountInline(admin.TabularInline):
	model = Account
	fields = ('id', 'email', 'phone')
	readonly_fields = ('id', 'email', 'phone')
	show_change_link = True
	extra = 0


class AccountInfoInline(admin.TabularInline):
	model = AccountInfo
	fields = ('id', 'first_name', 'last_name', 'title', 'team')
	readonly_fields = ('id', 'first_name', 'last_name', 'title', 'team')
	show_change_link = True
	extra = 0


class AccountAdmin(UserAdmin):
	# The forms to add and change user instances
	form = AccountChangeForm
	add_form = AccountCreationForm
	list_display = ('id', 'email', 'phone', 'is_staff')
	list_filter = ['is_staff']
	fieldsets = (
		(None, {'fields': ('email', 'phone', 'password')}),
		('Permissions', {'fields': ('is_staff', 'is_activated', 'is_verified')}),
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
	list_display = ('id', 'first_name', 'last_name', 'title', 'team')
	list_filter = ['is_staff']
	fieldsets = (
		('Personal info', {'fields': ('avatar', 'first_name', 'last_name', 'description', 'team')}),
		('Social Media', {'fields': ('linkedin', 'twitter', 'slack', 'telegram')}),
	)
	search_fields = ['first_name', 'last_name']
	inlines = [AccountInline]


class VerifyTokenAdmin(admin.ModelAdmin):
	list_display = ('email', 'phone', 'is_expired')
	fieldsets = (
		(None, {'fields': ('account', 'token', 'expire_time', 'is_expired')}),
	)
	readonly_fields = ('is_expired', 'expire_time')


class TeamAdmin(admin.ModelAdmin):
	list_display = ('name', 'description', 'created')
	fieldsets = [
		[None, {'fields': ['name', 'description', ]}],
		['Timestamp', {'fields': ['created', 'updated']}],
	]
	readonly_fields = ('created', 'updated')



admin.site.register(Account, AccountAdmin)
admin.site.register(VerifyToken, VerifyTokenAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.unregister(AdminGroup)
