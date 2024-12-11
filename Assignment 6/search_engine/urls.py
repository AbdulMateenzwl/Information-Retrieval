from django.urls import path
from . import views

urlpatterns = [
    path('', views.relevance_score_view, name='search'),
]