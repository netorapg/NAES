from django.urls import path
from .views import UsuarioCreateView
from django.contrib.auth import views as auth_views

app_name = 'usuarios'

urlpatterns = [
    path('registrar/', UsuarioCreateView.as_view(), name='registrar'),
    
    path('login/', auth_views.LoginView.as_view(
        template_name='usuarios/login.html'
    ), name='login'),

    path('logout/', auth_views.LogoutView.as_view(
        http_method_names=['get', 'post']
    ), name='logout'),
]