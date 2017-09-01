from django.contrib import admin

from .models import Discussion, Reply


class DiscussionAdmin(admin.ModelAdmin):
	fieldsets = (
		(None, {'fields': ('question', 'account')}),
		('Details', {'fields': ('title', 'content')}),
		('Timestamp', {'fields': ('created', 'updated')})
	)
	readonly_fields = ('created', 'updated')


class ReplyAdmin(admin.ModelAdmin):
	fieldsets = (
		(None, {'fields': ('question', 'account')}),
		('Details', {'fields': ('content',)}),
		('Timestamp', {'fields': ('created', 'updated')})
	)
	readonly_fields = ('created', 'updated')


admin.site.register(Discussion, DiscussionAdmin)
admin.site.register(Reply, ReplyAdmin)
