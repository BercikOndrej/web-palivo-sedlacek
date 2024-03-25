from django.urls import path
from django.views.generic.base import TemplateView
from . import views

app_name = 'website'
urlpatterns = [
    path('', views.index, name="index"),
    path('robots.txt/', views.robots_txt, name="robots_txt")
]