from django.urls import path
from . import views

app_name = 'pal40'

urlpatterns = [
    path('', views.index, name='index'),
    path('connector/<int:pk>/', views.connector_detail, name='connector_detail'),
    path('connector/<int:connector_pk>/pin/<int:pin_number>/', views.pin_detail, name='pin_detail'),
]
