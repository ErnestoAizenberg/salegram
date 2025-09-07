from django.contrib import admin
from .models import Product, Order, UserProfile

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['price', 'is_active']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'product', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user_id', 'product__name']
    readonly_fields = ['created_at', 'updated_at']
    actions = ['mark_as_delivered']

    def mark_as_delivered(self, request, queryset):
        queryset.update(status='delivered')
    mark_as_delivered.short_description = "Отметить как доставленные"

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'username', 'first_name', 'last_name', 'balance']
    search_fields = ['user_id', 'username', 'first_name', 'last_name']
    readonly_fields = ['created_at']
