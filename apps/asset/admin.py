from django.contrib import admin

from apps.asset.models import Asset

# Register your models here.

class AssetAdmin(admin.ModelAdmin):
    exclude = ('is_deleted',)  
admin.site.register(Asset, AssetAdmin) 