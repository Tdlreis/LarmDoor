from django.urls import path
from . import views
from .views import medias

urlpatterns = [
    path('graficos/', views.home, name="home"),
    path('medias/', views.medias, name="medias"),
    path('medias/<int:date_mode>/<str:start_date>/<str:end_date>/', medias, name='medias_with_dates'),

]