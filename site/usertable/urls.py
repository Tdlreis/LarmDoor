from django.urls import path
from . import views

urlpatterns = [
    path('', views.table, name='table'),
    path('delete/<int:pk>/<int:model>/', views.delete, name='delete'),
    path('edit/<int:pk>/<int:model>/', views.update, name='update'),
]

