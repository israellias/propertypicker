from django.contrib import admin

from properties.models import Zone


@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    pass
