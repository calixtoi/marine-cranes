from django.shortcuts import get_object_or_404, render
from .models import Connector, ControlSystem, Crane, Pin


def index(request):
    cranes = Crane.objects.prefetch_related('control_systems__connectors').all()
    return render(request, 'pal40/index.html', {'cranes': cranes})


def connector_detail(request, pk):
    connector = get_object_or_404(
        Connector.objects.select_related('control_system__crane'),
        pk=pk,
    )
    pins = connector.pins.select_related('device').prefetch_related(
        'safety_functions', 'signal_groups', 'troubleshooting'
    )
    signal_type_order = {'GND': 0, 'PWR': 1, 'CAN': 2, 'DI': 3, 'DO': 4, 'AI': 5, 'AO': 6}
    pins_by_type = {}
    for pin in pins:
        label = pin.get_signal_type_display()
        pins_by_type.setdefault(label, []).append(pin)
    return render(request, 'pal40/connector_detail.html', {
        'connector': connector,
        'pins': pins,
        'pins_by_type': pins_by_type,
    })


def pin_detail(request, connector_pk, pin_number):
    connector = get_object_or_404(Connector, pk=connector_pk)
    pin = get_object_or_404(
        Pin.objects.select_related('device', 'connector__control_system__crane')
                   .prefetch_related('safety_functions', 'signal_groups', 'troubleshooting'),
        connector=connector,
        pin_number=pin_number,
    )
    return render(request, 'pal40/pin_detail.html', {'pin': pin, 'connector': connector})
