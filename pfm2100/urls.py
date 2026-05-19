from django.urls import path
from . import views

app_name = 'pfm2100'

urlpatterns = [
    path('', views.device_list, name='device_list'),
    path('device/<int:pk>/', views.device_detail, name='device_detail'),
    path('wiring/<int:connector_pk>/', views.connector_wiring, name='connector_wiring'),
    path('map/', views.connector_map, name='connector_map'),
]
