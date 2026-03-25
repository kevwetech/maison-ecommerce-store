from django.contrib import admin
from .models import SiteConfig

# Register your models here.


@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
    list_display = ["site_name", "primary_color", "secondary_color"]