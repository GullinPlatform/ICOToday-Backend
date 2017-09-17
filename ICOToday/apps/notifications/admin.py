# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from models import Notification
from django.contrib import admin


class NotificationAdmin(admin.ModelAdmin):
	list_display = ['sender', 'receiver', 'read', 'created']


admin.site.register(Notification, NotificationAdmin)
