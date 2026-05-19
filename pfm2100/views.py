import json
from django.shortcuts import get_object_or_404, render
from django.core.serializers.json import DjangoJSONEncoder
from pal40.models import Connector as PAL40Connector
from .models import PFM2100Device


def device_list(request):
    devices = PFM2100Device.objects.prefetch_related('cables__wires').all()
    return render(request, 'pfm2100/device_list.html', {'devices': devices})


def device_detail(request, pk):
    device = get_object_or_404(
        PFM2100Device.objects.prefetch_related('cables__wires'),
        pk=pk,
    )
    return render(request, 'pfm2100/device_detail.html', {'device': device})


def connector_wiring(request, connector_pk):
    connector = get_object_or_404(PAL40Connector, pk=connector_pk)
    pins = connector.pins.select_related('device').order_by('pin_number')
    return render(request, 'pfm2100/connector_wiring.html', {
        'connector': connector,
        'pins': pins,
    })


def connector_map(request):
    connectors_qs = list(
        PAL40Connector.objects.prefetch_related('pins__device').order_by('designation')
    )

    conn_data = []
    for conn in connectors_qs:
        pins_data = []
        for pin in conn.pins.order_by('pin_number'):
            pins_data.append({
                'n':        pin.pin_number,
                'fn':       pin.function,
                'type':     pin.signal_type,
                'cable':    pin.cable or '',
                'wire':     pin.wire_color or '',
                'terminal': pin.terminal or '',
                'safety':   pin.safety_related,
                'device':   {
                    'id':    pin.device.identification,
                    'name':  pin.device.name,
                    'dtype': pin.device.get_device_type_display(),
                    'cable': pin.device.cable or '',
                } if pin.device else None,
                'conn_pk':    conn.pk,
                'conn_desig': conn.designation,
            })
        conn_data.append({
            'pk':          conn.pk,
            'designation': conn.designation,
            'color':       conn.color,
            'pins':        pins_data,
        })

    return render(request, 'pfm2100/connector_map.html', {
        'connectors':    connectors_qs,
        'pin_data_json': json.dumps({'connectors': conn_data}, cls=DjangoJSONEncoder),
    })
