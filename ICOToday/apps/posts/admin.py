from django.contrib import admin

from .models import Post, PostTag
from ..discussions.models import Comment


class CommentsInline(admin.TabularInline):
	model = Comment
	show_change_link = True
	extra = 1


class PostAdmin(admin.ModelAdmin):
	list_display = ('title', 'status', 'creator', 'start_datetime', 'end_datetime')

	fieldsets = (
		('Question Info', {'fields': ('title', 'status', 'creator')}),
		('Details', {'fields': ('team', 'description_short', 'promote_image', 'logo_image')}),
		('ICO Details', {'fields': ('maximum_goal', 'minimum_goal', 'coin_type', 'start_datetime', 'end_datetime', 'website', 'video_link', 'up_votes', 'down_votes', 'white_paper')}),
		('Timestamp', {'fields': ('created', 'updated')})
	)
	inlines = [CommentsInline]
	readonly_fields = ('created', 'updated')


class PostTagAdmin(admin.ModelAdmin):
	fieldsets = (('Tag', {'fields': ('tag',)}),)
	list_display = ('tag',)


class CommentsFieldAdmin(admin.ModelAdmin):
	fieldsets = (
		('Comments Field Info', {'fields': ('comment',)}),
	)


admin.site.register(Post, PostAdmin)
admin.site.register(PostTag, PostTagAdmin)
