from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .models import Label, Topic, Picture, Comment, SubComment, User

# Register your models here.
from datetime import date


class LabelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'create_time', 'visible']
    list_filter = ('selectable', 'visible')
    list_editable = ('visible',)


class PictureInline(admin.TabularInline):
    model = Picture
    extra = 1


# 添加admin动作（身份认证-成员确认）
def authority_check(self, request, queryset):
    queryset.update(authority=1, identity=0)
    # 操作完成后的提示信息
    self.message_user(request, '认证成功')


authority_check.short_description = "身份认证 - 成员确认"


class UserAdmin(admin.ModelAdmin):
    def preview(self, obj):
        # 返回方法2
        return format_html('<img src="/static/%s" height="32" />' % obj.avatar.url)

    preview.allow_tags = True
    preview.short_description = "头像"

    readonly_fields = ('openid', 'preview')
    list_display = ['id', 'preview', 'username', 'name', 'student_info', 'authority', 'identity']
    list_filter = ('grade', 'college', 'identity', 'authority', 'gender')
    fieldsets = (
        ['基本信息', {
            'fields': ('username', 'openid', 'preview', 'gender')}],
        ['身份验证', {
            'fields': ('identity', 'authority')}],
        ['学生信息', {
            'fields': ('college', 'grade', 'classes', 'name', 'phone')}]
    )
    ordering = ['-identity']
    actions = [authority_check]


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
    date_hierarchy = 'edit_time'
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
