from django.contrib import admin

from catalog.models import Category, Product


class ProductInline(admin.TabularInline):
    model = Product
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name_ar", "name_en", "slug")
    inlines = [ProductInline]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name_ar", "name_en", "price", "stock", "is_active", "category")
    list_filter = ("is_active", "category")
    search_fields = ("name_ar", "name_en")
