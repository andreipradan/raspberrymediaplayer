from django.contrib import admin

from .models import Station


@admin.register(Station)
class JobAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')
