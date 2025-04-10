from django.urls import path
from . import views

app_name = 'jogo'

urlpatterns = [
    path('', views.sinuca, name='home'),
    path('sobre/', views.sobre, name='sobre'),
]