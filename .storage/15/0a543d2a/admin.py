from django.contrib import admin
from .models import Category, Product, CartItem, Order, OrderItem, WishlistItem

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'available', 'category', 'created_at')
    list_filter = ('available', 'category', 'created_at')
    list_editable = ('price', 'stock', 'available')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'date_added')
    list_filter = ('date_added',)
    search_fields = ('user__username', 'product__name')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'full_name', 'total_amount', 'status', 'created_at', 'payment_status')
    list_filter = ('status', 'created_at', 'payment_status')
    search_fields = ('user__username', 'full_name', 'email', 'payment_id')
    inlines = [OrderItemInline]

class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ('wishlist', 'product', 'date_added')
    list_filter = ('date_added',)
    search_fields = ('wishlist__user__username', 'product__name')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(WishlistItem, WishlistItemAdmin)