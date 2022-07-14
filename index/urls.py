from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('msg/', views.publishMsg, name='pubMsg'),
    path('getInfo/', views.get_info, name='getInfo'),
    path('snap/', views.get_snap_img, name='snap'),
]
