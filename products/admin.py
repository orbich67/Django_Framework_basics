from django.contrib import admin

from products.models import ProductCategory, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'category', 'is_active')
    fields = (('name', 'is_active'), 'image', 'description', ('price', 'quantity'), 'category')
    readonly_fields = ('description',)
    ordering = ('name',)
    search_fields = ('name',)


@admin.register(ProductCategory)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
