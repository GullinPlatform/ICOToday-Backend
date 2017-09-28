# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Project, ProjectTag


class ProjectAdmin(admin.ModelAdmin):
	list_display = ('id', 'title', 'status', 'start_datetime', 'end_datetime')

	fieldsets = (
		('Relation Info', {'fields': ('company', 'status', 'creator')}),
		('Details', {'fields': ('title', 'logo_image', 'promote_image', 'category', 'description_short', 'description_full')}),
		('ICO Details', {'fields': ('type', 'coin_name', 'maximum_goal', 'minimum_goal', 'coin_unit', 'start_datetime', 'end_datetime', 'ratio', 'equality_on_offer', 'accept')}),
		('Supplement', {'fields': ('website', 'video_link', 'white_paper')}),
		('Media Info', {'fields': ('medium', 'twitter', 'slack', 'telegram')}),
		('Timestamp', {'fields': ('created', 'updated')})
	)
	readonly_fields = ('created', 'updated')


class PostTagAdmin(admin.ModelAdmin):
	fieldsets = (('Tag', {'fields': ('tag',)}),)
	list_display = ('tag',)


admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectTag, PostTagAdmin)
