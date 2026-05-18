from pal40.models import Connector
from pfm2100.models import PFM2100Device


def sidebar_nav(request):
    connectors = list(Connector.objects.select_related('control_system').order_by('designation'))
    devices = list(PFM2100Device.objects.only('id', 'description', 'part_number').order_by('order'))
    return {
        'nav_connectors': connectors,
        'nav_pfm_devices': devices,
    }
