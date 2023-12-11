from django.urls import path
from . import views

urlpatterns = [
    path('fetchrfid/', views.fetchrfid, name='fetchrfid'),
]