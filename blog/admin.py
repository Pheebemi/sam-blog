# blog/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from blog.models import Category, Comment, Post, CryptoUser

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

class CryptoUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'balance', 'total_invested', 'total_profit')
    fieldsets = UserAdmin.fieldsets + (
        ('Crypto Information', {'fields': ('phone_number', 'address', 'balance', 'total_invested', 'total_profit')}),
    )

admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(CryptoUser, CryptoUserAdmin)