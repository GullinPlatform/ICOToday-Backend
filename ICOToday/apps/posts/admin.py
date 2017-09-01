from django.contrib import admin

from .models import Post, PostTag
from ..accounts.models import Account


class PostAdmin(admin.ModelAdmin):
	fieldsets = (
		('Question Info', {'fields': ('title', 'status', 'creator')}),
		('Details', {'fields': ('description_short',)}),
		('ICO Details', {'fields': ('website', 'start_date', 'end_date', 'white_paper', 'up_votes', 'down_votes', 'video_link')}),
		('Timestamp', {'fields': ('created', 'updated')})
	)
	readonly_fields = ('created', 'updated')


class PostTagAdmin(admin.ModelAdmin):
	fieldsets = (('Tag', {'fields': ('tag',)}),)
	list_display = ('tag',)


admin.site.register(Post, PostAdmin)
admin.site.register(PostTag, PostTagAdmin)
