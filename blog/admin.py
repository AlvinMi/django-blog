# blog/admin.py

from django.contrib import admin
from .models import Post, Category, Tag

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_time', 'modified_time', 'category', 'author']

admin.site.register(Post, PostAdmin) # modfied 将新增的 PostAdmin 也加进来。
admin.site.register(Category)
admin.site.register(Tag)