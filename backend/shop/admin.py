from django.contrib import admin
from django.http import HttpRequest

from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "parent", "slug")
    ordering = ("name",)
    def get_prepopulated_fields(self, request, obj=None):
        return {"slug": ("name",),}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", 'brand', "discount", "price", 'created_at', 'updated_at')
    ordering = ("title",)
    list_filter = ('available', 'created_at', 'updated_at')
    
    def get_prepopulated_fields(self, request, obj=None):
        return {"slug": ("title",),}