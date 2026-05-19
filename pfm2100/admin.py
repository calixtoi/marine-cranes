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
    list_display = ('order', 'part_number', 'description', 'classification', 'connector_type', 'has_image', 'has_datasheet')
    list_display_links = ('part_number', 'description')
    list_editable = ('order',)
    inlines = [CableInline]
    fieldsets = (
        ('Device Identity', {
            'fields': ('order', 'part_number', 'description', 'classification',
                       'designation', 'type_function', 'signal_form', 'details',
                       'classification_notes', 'connector_type', 'connector_part_number'),
        }),
        ('Media & Documentation', {
            'fields': ('image', 'datasheet', 'datasheet_url'),
            'description': 'Upload a device photo (JPG/PNG) and/or a datasheet PDF. '
                           'An external URL can be used instead of or alongside the uploaded file.',
        }),
    )

    @admin.display(boolean=True, description='Photo')
    def has_image(self, obj):
        return bool(obj.image)

    @admin.display(boolean=True, description='Datasheet')
    def has_datasheet(self, obj):
        return bool(obj.datasheet or obj.datasheet_url)


@admin.register(PFM2100Cable)
class PFM2100CableAdmin(admin.ModelAdmin):
    list_display = ('cable_id', 'cable_part_number', 'connection_details', 'junction_box_ref', 'device')
    inlines = [WireTerminalInline]


@admin.register(PFM2100WireTerminal)
class WireTerminalAdmin(admin.ModelAdmin):
    list_display = ('wire_color', 'device_pin', 'terminal_ref', 'cable', 'notes')
