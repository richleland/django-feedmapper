from django.contrib import admin

from .models import Mapping


class MappingAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Mapping details", {
            'fields': ('label', 'source', 'parser', 'purge', 'data_map')
        }),
        ("Parsing results", {
            'fields': ('parse_attempted', 'parse_succeeded', 'parse_log')
        })
    )
    list_display = ('label', 'parser', 'purge', 'parse_attempted', 'parse_succeeded')
    list_filter = ('parser', 'parse_succeeded')
    readonly_fields = ('parse_log',)

admin.site.register(Mapping, MappingAdmin)
