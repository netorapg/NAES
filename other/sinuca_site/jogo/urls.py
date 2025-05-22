from django.urls import path
from . import views

app_name = 'jogo'

urlpatterns = [
    path('', views.sinuca, name='home'),
    path('sobre/', views.sobre, name='sobre'),
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('jogo/', views.jogo_view, name='jogo'),
    path('perfil/', views.perfil_view, name='perfil'),  # Adicione esta linha
    path('ranking/', views.ranking_view, name='ranking'),  # E esta também
]