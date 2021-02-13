from django.contrib import admin
from .models import ImageLabel, Tag, Good

# Register your models here.


class TagsAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'create_time']


class ImageInline(admin.TabularInline):
    model = ImageLabel
    extra = 1


class GoodsAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'price', 'seal_price', 'create_time']
    list_filter = ('out_of_stock', 'tag')
    inlines = [ImageInline, ]


admin.site.register(Tag, TagsAdmin)
admin.site.register(Good, GoodsAdmin)
