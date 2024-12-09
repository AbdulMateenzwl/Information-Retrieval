from django.urls import path
from django.shortcuts import render
from .views import get_presentation,hypertext_node_view

urlpatterns = [
    path('api/get-presentation/', get_presentation, name='get_presentation'),
    path('slides/', lambda request: render(request, 'slides.html'), name='slides'),
    path('node/<str:node>/', hypertext_node_view, name='hypertext_node'),
    path('node/', hypertext_node_view, name='hypertext_node'),  # Default to "home" node

]