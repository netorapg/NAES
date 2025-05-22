from django.urls import path
from . import views

app_name = 'jogo'

urlpatterns = [
    path('', views.sobre, name='home'),
    path('sobre/', views.sobre, name='sobre'),
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('sinuca/', views.sinuca_view, name='sinuca'),
    path('perfil/', views.perfil_view, name='perfil'), 
    path('ranking/', views.ranking_view, name='ranking'),
]