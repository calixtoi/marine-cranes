import json
from django.shortcuts import get_object_or_404, render, redirect
from django.core.serializers.json import DjangoJSONEncoder
from .models import PFM1200Device, PFM1200Cable
from .forms import make_wire_formset, CableMetaForm


def device_list(request):
    devices = PFM1200Device.objects.prefetch_related('cables__wires').all()
    return render(request, 'pfm1200/device_list.html', {'devices': devices})


def device_detail(request, order):
    device = get_object_or_404(
        PFM1200Device.objects.prefetch_related('cables__wires'),
        order=order,
    )
    return render(request, 'pfm1200/device_detail.html', {'device': device})


def edit_cable_wiring(request, cable_pk):
    cable = get_object_or_404(PFM1200Cable.objects.select_related('device'), pk=cable_pk)
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
            return redirect('pfm1200:device_detail', order=cable.device.order)
    else:
        formset = WireFormSet(queryset=cable.wires.order_by('order'))
        cable_form = CableMetaForm(instance=cable)
    return render(request, 'pfm1200/edit_cable_wiring.html', {
        'cable': cable,
        'device': cable.device,
        'formset': formset,
        'cable_form': cable_form,
    })


def wiring_diagram(request):
    from pfm1200.models import PFM1200Cable
    cables = PFM1200Cable.objects.select_related('device').prefetch_related('wires').order_by('device__order')
    cable_data = []
    for cable in cables:
        cable_data.append({
            'cable_id':    cable.cable_id,
            'device_ref':  cable.device.device_ref,
            'description': cable.device.description,
            'classification': cable.device.classification,
            'junction_box': cable.junction_box_ref,
            'length_mm':   cable.length_mm,
            'part_number': cable.cable_part_number,
            'wires': [
                {'order': w.order, 'color': w.wire_color,
                 'pin': w.device_pin, 'terminal': w.terminal_ref, 'notes': w.notes}
                for w in cable.wires.order_by('order')
            ],
        })
    return render(request, 'pfm1200/wiring_diagram.html', {
        'cable_data_json': json.dumps(cable_data, cls=DjangoJSONEncoder),
    })


def schematic(request):
    cables = PFM1200Cable.objects.select_related('device').prefetch_related('wires').all()
    device_data = {}
    for cable in cables:
        device_data[cable.cable_id] = {
            'device_order':   cable.device.order,
            'description':    cable.device.description,
            'part_number':    cable.device.part_number,
            'device_ref':     cable.device.device_ref,
            'classification': cable.device.classification,
            'cable_id':       cable.cable_id,
            'junction_box':   cable.junction_box_ref or '',
            'connection':     cable.connection_details or '',
            'wires': [
                {'pin': w.device_pin, 'color': w.wire_color, 'terminal': w.terminal_ref}
                for w in cable.wires.order_by('order')
            ],
        }
    return render(request, 'pfm1200/schematic.html', {
        'device_data_json': json.dumps(device_data, cls=DjangoJSONEncoder),
    })
