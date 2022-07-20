from django.contrib import admin
from .models import ContactModel, HomePageBannerModel


@admin.register(ContactModel)
class ContactModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'created_at']
    list_display_links = ['name', 'email']
    search_fields = ['name', 'email', 'message']
    list_filter = ['created_at']


@admin.register(HomePageBannerModel)
class HomePageBannerAdmin(admin.ModelAdmin):
    list_display = ['title', 'collections', 'is_active', 'created_at']
    list_display_links = ['title', 'collections']
    search_fields = ['title', 'collection']
    list_filter = ['created_at']
