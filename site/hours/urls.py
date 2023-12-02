from django.urls import path
from . import views

urlpatterns = [
    path('get-data/<int:cat>/<int:id>/', views.get_data, name='get_data'),
    path('hours/<int:id>/', views.hours, name='hours')
]
