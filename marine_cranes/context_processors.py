from pal40.models import Connector
from pfm2100.models import PFM2100Device
from pfm1200.models import PFM1200Device


def sidebar_nav(request):
    connectors = list(Connector.objects.select_related('control_system').order_by('designation'))
    devices = list(PFM2100Device.objects.only('id', 'device_ref', 'description', 'part_number').order_by('order'))
    devices_1200 = list(PFM1200Device.objects.only('id', 'order', 'device_ref', 'description', 'part_number').order_by('order'))
    return {
        'nav_connectors': connectors,
        'nav_pfm_devices': devices,
        'nav_pfm1200_devices': devices_1200,
    }
