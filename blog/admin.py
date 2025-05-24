# blog/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from blog.models import Category, Comment, Post, CryptoUser, Transaction, Balance

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

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan_name', 'amount', 'payment_method', 'status', 'transaction_date')
    list_filter = ('status', 'plan_name', 'payment_method')
    search_fields = ('user__username', 'plan_name')
    ordering = ('-transaction_date',)
    
    # Add action to mark transactions as completed
    actions = ['mark_as_completed']
    
    def mark_as_completed(self, request, queryset):
        queryset.update(status='completed')
    mark_as_completed.short_description = "Mark selected transactions as completed"

@admin.register(Balance)
class BalanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'last_updated')
    search_fields = ('user__username',)
    readonly_fields = ('last_updated',)
    
    def has_delete_permission(self, request, obj=None):
        return True  # Allow balance deletion

admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(CryptoUser, CryptoUserAdmin)