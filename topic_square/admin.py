from django.contrib import admin
from .models import Label, Topic

# Register your models here.

from datetime import date
from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class LabelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'pub_user', 'pub_time']


class TopicAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'user_name', 'create_time']
    list_filter = ('is_homework', 'labels_test')
    filter_horizontal = ('labels_test',)


admin.site.register(Label, LabelAdmin)
admin.site.register(Topic, TopicAdmin)
