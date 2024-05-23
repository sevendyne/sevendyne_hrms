from django.contrib import admin
from client.models import Client


class ClientAdmin(admin.ModelAdmin):
    exclude = ('date_added','is_deleted')  
admin.site.register(Client, ClientAdmin) 