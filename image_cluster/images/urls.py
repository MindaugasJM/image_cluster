from django.urls import path
from . import views

urlpatterns = [
    path('gallery', views.view_gallery, name='gallery'),
    path('upload_images/', views.upload_images, name='upload_images'),
    path('group_images/', views.activate_img_analysis, name='group_images'),
    path('delete_images/', views.delete_images, name='delete_images'),
]