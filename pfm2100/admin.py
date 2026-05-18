from django.contrib import admin
from .models import PFM2100Device, PFM2100Cable, PFM2100WireTerminal


class WireTerminalInline(admin.TabularInline):
    model = PFM2100WireTerminal
    extra = 0


class CableInline(admin.StackedInline):
    model = PFM2100Cable
    extra = 0
    show_change_link = True


@admin.register(PFM2100Device)
class PFM2100DeviceAdmin(admin.ModelAdmin):
    list_display = ('order', 'part_number', 'description', 'classification', 'connector_type')
    list_display_links = ('part_number', 'description')
    list_editable = ('order',)
    inlines = [CableInline]


@admin.register(PFM2100Cable)
class PFM2100CableAdmin(admin.ModelAdmin):
    list_display = ('cable_id', 'cable_part_number', 'connection_details', 'junction_box_ref', 'device')
    inlines = [WireTerminalInline]


@admin.register(PFM2100WireTerminal)
class WireTerminalAdmin(admin.ModelAdmin):
    list_display = ('wire_color', 'device_pin', 'terminal_ref', 'cable', 'notes')
