from django.shortcuts import get_object_or_404, render
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
