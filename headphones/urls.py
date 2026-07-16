from django.urls import path
from . import views


urlpatterns = [
    path('', views.headphones_list, name='headphones_list'),
    path('<str:model>/', views.headphone_detail, name='headphone_detail'),
]