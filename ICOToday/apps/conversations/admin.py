# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Message


class MessageAdmin(admin.ModelAdmin):
	list_display = ('id', 'content', 'creator', 'created', 'read')
	fieldsets = (
		('Details', {'fields': ('creator', 'content', 'read',)}),

		('Timestamp', {'fields': ('created', 'updated')})
	)
	readonly_fields = ('created', 'updated')


admin.site.register(Message, MessageAdmin)
