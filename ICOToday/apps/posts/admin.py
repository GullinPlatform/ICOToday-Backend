from django.contrib import admin

from .models import Post, PostTag
from .models import Post, PostTag, CommentsField


class CommentsFieldInline(admin.TabularInline):
	model = CommentsField


class PostAdmin(admin.ModelAdmin):
	list_display = ('title', 'status', 'creator', 'start_datetime', 'start_datetime')

	fieldsets = (
		('Question Info', {'fields': ('title', 'status', 'creator')}),
		('Details', {'fields': ('description_short', 'promote_image', 'logo_image')}),
		('ICO Details', {'fields': ('start_datetime', 'start_datetime', 'website', 'video_link', 'up_votes', 'down_votes', 'white_paper',)}),
		('Timestamp', {'fields': ('created', 'updated')})
	)
	inlines = [CommentsFieldInline]
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
