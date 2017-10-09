# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Project, ProjectTag, ProjectRatingDetail


class ProjectAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'status', 'start_datetime', 'end_datetime')

	fieldsets = (
		('Relation Info', {'fields': ('company', 'status')}),
		('Details', {'fields': ('name', 'logo_image', 'promote_image', 'category', 'description_short', 'description_full')}),
		('ICO Details', {'fields': ('type', 'coin_name', 'maximum_goal', 'minimum_goal', 'coin_unit', 'start_datetime', 'end_datetime', 'ratio', 'equality_on_offer', 'accept')}),
		('Supplement', {'fields': ('website', 'video_link', 'white_paper')}),
		('Media Info', {'fields': ('medium', 'twitter', 'slack', 'telegram')}),
		('Timestamp', {'fields': ('created', 'updated')})
	)
	readonly_fields = ('created', 'updated')


class PostTagAdmin(admin.ModelAdmin):
	fieldsets = (('Tag', {'fields': ('tag',)}),)
	list_display = ('tag',)


class ProjectRatingDetailAdmin(admin.ModelAdmin):
	list_display = ('rater', 'score', 'project', 'created')

	fieldsets = (('Info', {'fields': ('rater', 'project')}),
	             ('Detail', {'fields': ('score', 'content')}),
	             ('Timestamp', {'fields': ('created', 'updated')}),)
	readonly_fields = ('created', 'updated')


admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectTag, PostTagAdmin)
admin.site.register(ProjectRatingDetail, ProjectRatingDetailAdmin)
