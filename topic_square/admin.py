from django.contrib import admin
from .models import Label, Topic, Picture, Comments, SubComments, User

# Register your models here.

from datetime import date
from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class LabelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'create_time']


class PictureInline(admin.TabularInline):
    model = Picture
    extra = 1


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'nickname', 'grade', 'college']
    list_filter = ('grade', 'college')


class SubCommentInline(admin.StackedInline):
    readonly_fields = ('like_count', 'likes',)
    model = SubComments
    extra = 0


class CommentInline(admin.StackedInline):
    readonly_fields = ('like_count', 'likes',)
    model = Comments
    extra = 0
    inlines = [SubCommentInline]


class TopicAdmin(admin.ModelAdmin):
    readonly_fields = ('like_count', 'likes', 'view_count', 'views', 'stars')
    list_display = ['id', 'title', 'create_time']
    list_filter = ('is_homework', 'labels')
    filter_horizontal = ('labels',)
    fieldsets = (
        ['正文内容', {
            'fields': ('labels', 'title', 'user',
                       'content', 'is_homework')}],
        ['互动内容', {
            'fields': (('like_count', 'likes'),
                       ('view_count', 'views'), 'stars')}]
    )
    inlines = [PictureInline, CommentInline]


admin.site.register(Label, LabelAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(User, UserAdmin)
