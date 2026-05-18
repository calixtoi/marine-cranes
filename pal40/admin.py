from django.contrib import admin
from .models import (
    Crane, ControlSystem, Connector, Device,
    Pin, SignalGroup, SafetyFunction, TroubleshootingNote,
)


@admin.register(Crane)
class CraneAdmin(admin.ModelAdmin):
    list_display = ('name', 'model_number', 'serial_number')


@admin.register(ControlSystem)
class ControlSystemAdmin(admin.ModelAdmin):
    list_display = ('name', 'model', 'crane', 'safety_level')


@admin.register(Connector)
class ConnectorAdmin(admin.ModelAdmin):
    list_display = ('designation', 'color', 'connector_type', 'control_system')


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('identification', 'name', 'device_type', 'cable')
    list_filter = ('device_type',)


class TroubleshootingInline(admin.TabularInline):
    model = TroubleshootingNote
    extra = 0


@admin.register(Pin)
class PinAdmin(admin.ModelAdmin):
    list_display = ('pin_number', 'connector', 'signal_type', 'direction', 'function', 'device', 'safety_related')
    list_filter = ('connector', 'signal_type', 'direction', 'safety_related')
    search_fields = ('function', 'cable', 'wire_color', 'terminal')
    inlines = [TroubleshootingInline]


@admin.register(SignalGroup)
class SignalGroupAdmin(admin.ModelAdmin):
    filter_horizontal = ('pins',)


@admin.register(SafetyFunction)
class SafetyFunctionAdmin(admin.ModelAdmin):
    list_display = ('name', 'safety_level', 'reaction_time_ms')
    filter_horizontal = ('pins',)


@admin.register(TroubleshootingNote)
class TroubleshootingNoteAdmin(admin.ModelAdmin):
    list_display = ('pin', 'symptom', 'likely_cause')
