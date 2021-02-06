from django.contrib import admin
from .models import Label, Topic, Picture

# Register your models here.

from datetime import date
from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class LabelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'pub_user', 'pub_time']


class PictureInline(admin.TabularInline):
    model = Picture
    extra = 1


class TopicAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'user_name', 'create_time']
    list_filter = ('is_homework', 'labels')
    filter_horizontal = ('labels',)
    fieldsets = (
        ['正文内容', {
            'fields': ('labels', 'title', 'user_name', 'user_id', 'avatar',
                       'content', 'is_homework')}],
        ['互动内容', {
            'fields': (('comment_count', 'comments'),
                       ('star_count', 'stars'),
                       ('view_count', 'views'))}]
    )
    inlines = [PictureInline]


admin.site.register(Label, LabelAdmin)
admin.site.register(Topic, TopicAdmin)
