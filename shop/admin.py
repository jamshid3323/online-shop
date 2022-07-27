from django.contrib import admin
from .models import ProductTagModel, ProductModel, CategoryModel, ProductBrandModel, ProductColorModel, ProductSizeModel
from .forms import ColorModelAdminForm
from django.utils.safestring import mark_safe


@admin.register(ProductTagModel)
class ProductTagModelAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_display_links = ['name']
    search_fields = ['name']


@admin.register(ProductSizeModel)
class ProductSizeModelAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_display_links = ['name']
    search_fields = ['name']


@admin.register(ProductBrandModel)
class ProductBrandModelAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_display_links = ['name']
    search_fields = ['name']


@admin.register(ProductColorModel)
class ProductColorModelAdmin(admin.ModelAdmin):
    list_display = ['code', 'color']
    list_display_links = ['code']
    search_fields = ['code']
    form = ColorModelAdminForm

    def color(self, object):
        free_space = '&nbsp;' * 2
        return mark_safe(f"<div style='background-color: {object.code}; width: 40px;'>{free_space}</div>")


@admin.register(CategoryModel)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_display_links = ['name']
    search_fields = ['name']


@admin.register(ProductModel)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'real_price', 'discount', 'sale', 'created_at']
    list_display_links = ['title', 'price', 'created_at']
    list_filter = ['created_at']
    search_fields = ['title', 'price']
    autocomplete_fields = ['category', 'tag', 'size', 'color']
    readonly_fields = ['real_price', 'sale']
