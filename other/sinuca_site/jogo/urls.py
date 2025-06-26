from django.urls import path
from . import views

app_name = 'jogo'

urlpatterns = [
    # Rotas principais
    path('', views.home, name='home'),
    path('sobre/', views.sobre, name='sobre'),
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/', views.perfil_view, name='perfil'), 
    path('ranking/', views.ranking_view, name='ranking'),
    
    # Rotas do jogo
    path('sinuca/', views.sinuca_view, name='sinuca'),
    path('criar-mesa/', views.criar_mesa, name='criar_mesa'),
    path('entrar-mesa/<uuid:mesa_id>/', views.entrar_mesa, name='entrar_mesa'),
    path('sair-mesa/<uuid:mesa_id>/', views.sair_mesa, name='sair_mesa'),
    path('excluir-mesa/<uuid:mesa_id>/', views.excluir_mesa, name='excluir_mesa'),
    path('jogar/<uuid:mesa_id>/', views.jogar, name='jogar'),
    
    # CRUD de usuários (admin)
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('users/<uuid:pk>/edit/', views.UserUpdateView.as_view(), name='user_edit'),
    path('users/<uuid:pk>/delete/', views.UserDeleteView.as_view(), name='user_delete'),
    path('users/create/', views.UserCreateView.as_view(), name='user_create'),
]