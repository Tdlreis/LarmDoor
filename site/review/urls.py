from django.urls import path
from . import views

urlpatterns = [
    path('reviewlist/', views.reviewlist, name='reviewlist'),
    path('review/<int:id>/', views.review, name='review'),
    path('review/<int:id>/delete/', views.delete, name='delete'),
]
