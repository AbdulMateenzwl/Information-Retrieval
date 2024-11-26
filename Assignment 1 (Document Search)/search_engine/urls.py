from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_view, name='search'),
    path('upload/', views.upload_file_view, name='upload_file'),
]