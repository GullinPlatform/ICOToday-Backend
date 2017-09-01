from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group as AdminGroup

from .forms import AccountChangeForm, AccountCreationForm
from .models import Account, VerifyToken, AccountVerifyInfo


class AccountAdmin(UserAdmin):
	# The forms to add and change user instances
	form = AccountChangeForm
	add_form = AccountCreationForm
	list_display = ('id', 'email', 'username', 'is_staff')
	list_filter = ['is_staff']
	fieldsets = (
		(None, {'fields': ('email', 'username', 'password')}),
		('Personal info', {'fields': ('first_name', 'last_name')}),
		('Permissions', {'fields': ('is_staff', 'is_activated', 'is_company', 'is_verified')}),
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


class AccountVerifyInfoAdmin(admin.ModelAdmin):
	list_display = ('account', 'created', 'updated')
	fieldsets = (
		(None, {'fields': ('account', 'created', 'updated')}),
		('Individual',
		 {'fields': ('real_name', 'birthday', 'working_at', 'legal_id', 'legal_id_type', 'wechat', 'qq', 'phone',)}),
		('Company',
		 {'fields': ('company_name', 'company_register_file', 'company_phone', 'company_contact', 'company_email',
		             'company_address', 'company_field',)}),
	)
	readonly_fields = ('created', 'updated')


admin.site.register(Account, AccountAdmin)
admin.site.register(VerifyToken, VerifyTokenAdmin)
admin.site.register(AccountVerifyInfo, AccountVerifyInfoAdmin)
admin.site.unregister(AdminGroup)
