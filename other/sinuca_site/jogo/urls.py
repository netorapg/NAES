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
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('users/<int:pk>/edit/', views.UserUpdateView.as_view(), name='user_edit'),
    path('users/<int:pk>/delete/', views.UserDeleteView.as_view(), name='user_delete'),
    path('users/create/', views.UserCreateView.as_view(), name='user_create'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user_detail'),
]