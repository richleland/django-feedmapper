from django.contrib import admin

from .models import Mapping


class MappingAdmin(admin.ModelAdmin):
    pass

admin.site.register(Mapping, MappingAdmin)
