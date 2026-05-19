import json
from django.shortcuts import get_object_or_404, render, redirect
from django.core.serializers.json import DjangoJSONEncoder
from pal40.models import Connector as PAL40Connector
from .models import PFM2100Device, PFM2100Cable
from .forms import make_wire_formset, CableMetaForm


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


def edit_cable_wiring(request, cable_pk):
    cable = get_object_or_404(PFM2100Cable.objects.select_related('device'), pk=cable_pk)
    WireFormSet = make_wire_formset(extra=1)
    if request.method == 'POST':
        formset = WireFormSet(request.POST, queryset=cable.wires.order_by('order'))
        cable_form = CableMetaForm(request.POST, instance=cable)
        if formset.is_valid() and cable_form.is_valid():
            cable_form.save()
            instances = formset.save(commit=False)
            for obj in formset.deleted_objects:
                obj.delete()
            for instance in instances:
                instance.cable = cable
                instance.save()
            return redirect('pfm2100:device_detail', pk=cable.device.pk)
    else:
        formset = WireFormSet(queryset=cable.wires.order_by('order'))
        cable_form = CableMetaForm(instance=cable)
    return render(request, 'pfm2100/edit_cable_wiring.html', {
        'cable': cable,
        'device': cable.device,
        'formset': formset,
        'cable_form': cable_form,
    })


def schematic(request):
    cables = PFM2100Cable.objects.select_related('device').prefetch_related('wires').all()
    device_data = {}
    for cable in cables:
        device_data[cable.cable_id] = {
            'device_pk':    cable.device.pk,
            'description':  cable.device.description,
            'part_number':  cable.device.part_number,
            'classification': cable.device.classification,
            'cable_id':     cable.cable_id,
            'junction_box': cable.junction_box_ref or '',
            'connection':   cable.connection_details or '',
            'wires': [
                {'pin': w.device_pin, 'color': w.wire_color, 'terminal': w.terminal_ref}
                for w in cable.wires.order_by('order')
            ],
        }
    return render(request, 'pfm2100/schematic.html', {
        'device_data_json': json.dumps(device_data, cls=DjangoJSONEncoder),
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
