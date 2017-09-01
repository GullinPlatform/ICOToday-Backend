from django.contrib import admin

from .models import Post, PostTag


class PostAdmin(admin.ModelAdmin):
	fieldsets = (
		('Question Info', {'fields': ('title', 'creator', 'status', 'due_date', 'appliers')}),
		('Details', {'fields': ('description_short', 'prize', 'difficulty', 'industry_tags', 'tech_tags')}),
		('ICO Details', {'fields': ('website', 'start_date', 'end_date', 'white_paper', 'upvotes', 'downvotes', 'video_link', 'team_members')}),
		('Timestamp', {'fields': ('created', 'updated')})
	)
	readonly_fields = ('created', 'updated')


class PostTagAdmin(admin.ModelAdmin):
	fieldsets = (('Tag', {'fields': ('tag',)}),)
	list_display = ('tag',)


admin.site.register(Post, PostAdmin)
admin.site.register(PostTag, PostTagAdmin)
