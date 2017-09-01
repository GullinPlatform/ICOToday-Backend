from django.contrib import admin

from .models import Post, QuestionField, QuestionFile, QuestionTag


class QuestionFieldInline(admin.TabularInline):
	model = QuestionField


class QuestionFileInline(admin.TabularInline):
	model = QuestionFile


class PostAdmin(admin.ModelAdmin):
	fieldsets = (
		('Question Info', {'fields': ('title', 'creator', 'status', 'due_date', 'appliers')}),
		('Details', {'fields': ('description_short', 'prize', 'difficulty', 'industry_tags', 'tech_tags')}),
		('Timestamp', {'fields': ('created', 'updated')})
	)
	inlines = [QuestionFieldInline, QuestionFileInline]
	readonly_fields = ('created', 'updated')


class QuestionFieldAdmin(admin.ModelAdmin):
	fieldsets = (
		('Question Field Info', {'fields': ('title', 'content', 'question')}),
	)


class QuestionTagAdmin(admin.ModelAdmin):
	fieldsets = (('Tag', {'fields': ('type', 'tag')}),)
	list_display = ('tag', 'type')


class QuestionFileAdmin(admin.ModelAdmin):
	fieldsets = (
		('Question File Info', {'fields': ('file', 'question')}),
	)


admin.site.register(Post, PostAdmin)
admin.site.register(QuestionField, QuestionFieldAdmin)
admin.site.register(QuestionFile, QuestionFileAdmin)
admin.site.register(QuestionTag, QuestionTagAdmin)
