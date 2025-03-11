# blog/admin.py

from django.contrib import admin
from blog.models import Category, Comment, Post

class CategoryAdmin(admin.ModelAdmin):
    pass

class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "created_on", "last_modified")
    search_fields = ["title"]
    readonly_fields = ('created_on', 'last_modified')
    filter_horizontal = ("categories",)
    pass

class CommentAdmin(admin.ModelAdmin):
    pass

admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)