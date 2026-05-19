from django.shortcuts import get_object_or_404, render
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
