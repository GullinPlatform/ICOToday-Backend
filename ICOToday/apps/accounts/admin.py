from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group as AdminGroup

from .forms import AccountChangeForm, AccountCreationForm
from .models import Account, VerifyToken, AccountVerifyInfo, Team


class AccountInline(admin.TabularInline):
	model = Account
	fields = ('id', 'email', 'phone')
	readonly_fields = ('id', 'email', 'phone')
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
		('Personal info', {'fields': ('first_name', 'last_name', 'team')}),
		('Permissions', {'fields': ('is_staff', 'is_activated', 'is_verified')}),
		('Timestamp', {'fields': ('created', 'updated')})
	)
	readonly_fields = ('created', 'updated', 'is_staff',)
	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields' : ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')}
		 ),
	)
	search_fields = ('email', 'username')
	ordering = ('email',)


class VerifyTokenAdmin(admin.ModelAdmin):
	list_display = ('email', 'phone', 'is_expired')
	fieldsets = (
		(None, {'fields': ('account', 'token', 'expire_time', 'is_expired')}),
	)
	readonly_fields = ('is_expired', 'expire_time')


# class AccountVerifyInfoAdmin(admin.ModelAdmin):
# 	list_display = ('account', 'created', 'updated')
# 	fieldsets = (
# 		(None, {'fields': ('account', 'created', 'updated')}),
# 		('Individual',
# 		 {'fields': ('real_name', 'birthday', 'working_at', 'legal_id', 'legal_id_type', 'wechat', 'qq', 'phone',)}),
# 		('Company',
# 		 {'fields': ('company_name', 'company_register_file', 'company_phone', 'company_contact', 'company_email',
# 		             'company_address', 'company_field',)}),
# 	)
# 	readonly_fields = ('created', 'updated')

class TeamAdmin(admin.ModelAdmin):
	list_display = ('name', 'description', 'created')
	fieldsets = [
		[None, {'fields': ['name', 'description', ]}],
		['Timestamp', {'fields': ['created', 'updated']}],
	]
	readonly_fields = ('created', 'updated')
	inlines = [AccountInline]


admin.site.register(Account, AccountAdmin)
admin.site.register(VerifyToken, VerifyTokenAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.unregister(AdminGroup)
