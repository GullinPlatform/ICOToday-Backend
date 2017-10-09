# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from models import Notification
from django.contrib import admin


class NotificationAdmin(admin.ModelAdmin):
	list_display = ['receiver', 'sender', 'read', 'created', 'related']
	fieldsets = (
		('Permissions', {'fields': ('receiver', 'sender', 'content')}),
		('Other', {'fields': ('read', 'related')}),
		('Timestamp', {'fields': ('created', 'updated')})
	)
	readonly_fields = ('created', 'updated',)


admin.site.register(Notification, NotificationAdmin)
