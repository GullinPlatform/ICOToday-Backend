from django.contrib import admin

from .models import Post, PostTag, RatingDetail
from ..discussions.models import Comment


class CommentsInline(admin.TabularInline):
	model = Comment
	show_change_link = True
	extra = 1


class PostAdmin(admin.ModelAdmin):
	list_display = ('id', 'title', 'status', 'creator', 'start_datetime', 'end_datetime')

	fieldsets = (
		('Relation Info', {'fields': ('team', 'status', 'creator')}),
		('Details', {'fields': ('title', 'logo_image', 'promote_image', 'category', 'description_short', 'description_full')}),
		('ICO Details', {'fields': ('type', 'coin_name', 'maximum_goal', 'minimum_goal', 'coin_unit', 'start_datetime', 'end_datetime', 'ratio', 'equality_on_offer', 'accept')}),
		('Supplement', {'fields': ('website', 'video_link', 'white_paper')}),
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
		('Details', {'fields': ('detail',)}),
		('Timestamp', {'fields': ('created', 'updated')})
	)
	readonly_fields = ('created', 'updated')


admin.site.register(Post, PostAdmin)
admin.site.register(PostTag, PostTagAdmin)
admin.site.register(RatingDetail, RatingDetailAdmin)
