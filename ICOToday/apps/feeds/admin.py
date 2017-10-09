# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Feed


class FeedAdmin(admin.ModelAdmin):
	list_display = ('id', 'type', 'creator', 'created')
	fieldsets = (
		('Details', {'fields': ('content', 'reply_to', 'type', 'creator')}),
		('Relations', {'fields': ('company',)}),
		('Timestamp', {'fields': ('created', 'updated')})
	)
	readonly_fields = ('created', 'updated')


admin.site.register(Feed, FeedAdmin)
