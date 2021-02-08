from django.contrib import admin
from .models import Label, Topic, Picture, Comments

# Register your models here.

from datetime import date
from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class LabelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'user_name', 'create_time']


class PictureInline(admin.TabularInline):
    model = Picture
    extra = 1


class CommentInline(admin.StackedInline):
    model = Comments
    extra = 0


class TopicAdmin(admin.ModelAdmin):
    readonly_fields = ('star_count', 'stars', 'view_count', 'views',)
    list_display = ['id', 'title', 'user_name', 'create_time']
    list_filter = ('is_homework', 'labels')
    filter_horizontal = ('labels',)
    fieldsets = (
        ['正文内容', {
            'fields': ('labels', 'title', 'user_name', 'user_id', 'avatar',
                       'content', 'is_homework')}],
        ['互动内容', {
            'fields': (('star_count', 'stars'),
                       ('view_count', 'views'))}]
    )
    inlines = [PictureInline, CommentInline]


admin.site.register(Label, LabelAdmin)
admin.site.register(Topic, TopicAdmin)
