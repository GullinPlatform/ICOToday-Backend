# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Company


class CompanyAdmin(admin.ModelAdmin):
	list_display = ('name', 'description', 'created')
	fieldsets = [
		[None, {'fields': ['name', 'description', ]}],
		['Timestamp', {'fields': ['created', 'updated']}],
	]
	readonly_fields = ('created', 'updated')


admin.site.register(Company, CompanyAdmin)
