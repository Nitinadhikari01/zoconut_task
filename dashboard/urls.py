from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('get-clients-table/', views.get_clients_table, name='get_clients_table'),
    path('add-client/', views.add_client, name='add_client'),
]