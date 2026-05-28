from django.contrib import admin
from .models import PFM1200Device, PFM1200Cable, PFM1200WireTerminal


class WireTerminalInline(admin.TabularInline):
    model = PFM1200WireTerminal
    extra = 0


class CableInline(admin.StackedInline):
    model = PFM1200Cable
    extra = 0
    show_change_link = True


@admin.register(PFM1200Device)
class PFM1200DeviceAdmin(admin.ModelAdmin):
    list_display = ('order', 'device_ref', 'part_number', 'description', 'classification', 'connector_type', 'has_image', 'has_datasheet')
    list_display_links = ('device_ref', 'part_number', 'description')
    list_editable = ('order',)
    inlines = [CableInline]
    fieldsets = (
        ('Device Identity', {
            'fields': ('order', 'device_ref', 'part_number', 'description', 'classification',
                       'designation', 'type_function', 'signal_form', 'details',
                       'classification_notes', 'connector_type', 'connector_part_number'),
        }),
        ('Media & Documentation', {
            'fields': ('image', 'datasheet', 'datasheet_url'),
        }),
    )

    @admin.display(boolean=True, description='Photo')
    def has_image(self, obj):
        return bool(obj.image)

    @admin.display(boolean=True, description='Datasheet')
    def has_datasheet(self, obj):
        return bool(obj.datasheet or obj.datasheet_url)


@admin.register(PFM1200Cable)
class PFM1200CableAdmin(admin.ModelAdmin):
    list_display = ('cable_id', 'cable_part_number', 'connection_details', 'length_mm', 'junction_box_ref', 'device')
    inlines = [WireTerminalInline]


@admin.register(PFM1200WireTerminal)
class WireTerminalAdmin(admin.ModelAdmin):
    list_display = ('wire_color', 'device_pin', 'terminal_ref', 'cable', 'notes')
