from django.contrib import admin

from .models import Post, PostTag, RatingDetail
from ..discussions.models import Comment


class CommentsInline(admin.TabularInline):
	model = Comment
	show_change_link = True
	extra = 1


class PostAdmin(admin.ModelAdmin):
	list_display = ('title', 'status', 'creator', 'start_datetime', 'end_datetime')

	fieldsets = (
		('Question Info', {'fields': ('title', 'status', 'creator')}),
		('Details', {'fields': ('team', 'description_short', 'description_full', 'promote_image', 'logo_image')}),
		('ICO Details', {'fields': ('maximum_goal', 'minimum_goal', 'coin_type', 'start_datetime', 'end_datetime', 'website', 'video_link', 'white_paper')}),
		('Media Info', {'fields': ('medium', 'twitter', 'slack', 'telegram')}),
		('Timestamp', {'fields': ('created', 'updated')})
	)
	inlines = [CommentsInline]
	readonly_fields = ('created', 'updated')


class PostTagAdmin(admin.ModelAdmin):
	fieldsets = (('Tag', {'fields': ('tag',)}),)
	list_display = ('tag',)


class RatingDetailAdmin(admin.ModelAdmin):
	list_display = ('rater', 'post', 'created',)
	fieldsets = (
		('Info', {'fields': ('rater', 'post')}),
		('Details', {'fields': ('description',)}),
		('Timestamp', {'fields': ('created', 'updated')})
	)
	readonly_fields = ('created', 'updated')


admin.site.register(Post, PostAdmin)
admin.site.register(PostTag, PostTagAdmin)
admin.site.register(RatingDetail, RatingDetailAdmin)
