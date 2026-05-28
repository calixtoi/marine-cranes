from django.urls import path
from . import views

app_name = 'pfm1200'

urlpatterns = [
    path('', views.device_list, name='device_list'),
    path('device/<int:order>/', views.device_detail, name='device_detail'),
    path('wiring/', views.wiring_diagram, name='wiring_diagram'),
    path('schematic/', views.schematic, name='schematic'),
    path('cable/<int:cable_pk>/edit/', views.edit_cable_wiring, name='edit_cable_wiring'),
]
