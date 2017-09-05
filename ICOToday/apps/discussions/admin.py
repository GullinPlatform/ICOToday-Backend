from django.contrib import admin

from .models import Comment, Message


class DiscussionAdmin(admin.ModelAdmin):
	fieldsets = (
		(None, {'fields': ('question', 'account')}),
		('Details', {'fields': ('title', 'content')}),
		('Timestamp', {'fields': ('created', 'updated')})
	)
	readonly_fields = ('created', 'updated')


class CommentAdmin(admin.ModelAdmin):
	list_display = ('id', 'post', 'account', 'created')
	fieldsets = (
		(None, {'fields': ('post', 'account')}),
		('Details', {'fields': ('content', 'reply_to')}),
		('Timestamp', {'fields': ('created', 'updated')})
	)
	readonly_fields = ('created', 'updated')


admin.site.register(Comment, CommentAdmin)
