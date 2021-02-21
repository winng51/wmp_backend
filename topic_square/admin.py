from django.contrib import admin
from .models import Label, Topic, Picture, Comment, SubComment, User

# Register your models here.

from datetime import date
from django.utils.translation import gettext_lazy as _


class LabelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'create_time']


class PictureInline(admin.TabularInline):
    model = Picture
    extra = 1


class UserAdmin(admin.ModelAdmin):
    readonly_fields = ('openid',)
    list_display = ['id', 'name', 'college', 'grade', 'classes']
    list_filter = ('grade', 'college', 'identity', 'authority', 'gender')


class SubCommentInline(admin.StackedInline):
    readonly_fields = ('like_count', 'likes',)
    model = SubComment
    extra = 0


class CommentAdmin(admin.ModelAdmin):
    readonly_fields = ('like_count', 'likes',)
    list_display = ['id', '__str__', 'content']
    list_filter = ('topic', 'user')
    inlines = [SubCommentInline]


class CommentInline(admin.StackedInline):
    readonly_fields = ('like_count', 'likes',)
    model = Comment
    extra = 0


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


admin.site.register(User, UserAdmin)
admin.site.register(Label, LabelAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Comment, CommentAdmin)
