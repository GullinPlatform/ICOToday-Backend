# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Project, ProjectTag, ProjectRatingDetail


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'status', 'start_datetime', 'end_datetime')

	fieldsets = (
		('Relation Info', {'fields': ('company', 'status', 'rating')}),
		('Details', {'fields': ('name', 'logo_image', 'promote_image', 'category', 'description_short', 'description_full', 'token_sale_plan')}),
		('ICO Details', {'fields': ('type', 'coin_name', 'initial_price', 'maximum_goal', 'minimum_goal', 'coin_unit', 'start_datetime', 'end_datetime', 'ratio', 'equality_on_offer', 'accept')}),
		('Supplement', {'fields': ('website', 'video_link', 'white_paper')}),
		('Media Info', {'fields': ('medium', 'twitter', 'slack', 'telegram')}),
		('Timestamp', {'fields': ('created', 'updated')})
	)
	readonly_fields = ('created', 'updated')


@admin.register(ProjectTag)
class ProjectTagAdmin(admin.ModelAdmin):
	fieldsets = (('Tag', {'fields': ('tag',)}),)
	list_display = ('tag',)


@admin.register(ProjectRatingDetail)
class ProjectRatingDetailAdmin(admin.ModelAdmin):
	list_display = ('id', 'rater', 'score', 'project', 'created')

	fieldsets = (('Info', {'fields': ('rater', 'project')}),
	             ('Detail', {'fields': ('score', 'content', 'file')}),
	             ('Timestamp', {'fields': ('created', 'updated')}),)
	readonly_fields = ('created', 'updated')
