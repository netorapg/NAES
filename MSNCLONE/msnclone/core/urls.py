# msnclone/core/urls.py
from django.urls import path
from .views import (
    HomeView, StatusListView, StatusCreateView, StatusUpdateView, StatusDeleteView, 
    UserListView, EnviarPedidoAmizadeView, MeusContatosView, ResponderPedidoAmizadeView
)
app_name = 'core'

urlpatterns = [
    # URL da Home
    path('', HomeView.as_view(), name='home'),

    # URLs do CRUD de Status
    path('status/', StatusListView.as_view(), name='status-list'),
    path('status/cadastrar/', StatusCreateView.as_view(), name='status-create'),
    path('status/editar/<int:pk>/', StatusUpdateView.as_view(), name='status-update'),
    path('status/excluir/<int:pk>/', StatusDeleteView.as_view(), name='status-delete'),
    
    # URLs de usuários e amizades
    path('usuarios/', UserListView.as_view(), name='user-list'),
    path('adicionar-amigo/<int:pk>/', EnviarPedidoAmizadeView.as_view(), name='adicionar-amigo'),
    path('meus-contatos/', MeusContatosView.as_view(), name='meus-contatos'),
    path('responder-pedido/<int:pk>/', ResponderPedidoAmizadeView.as_view(), name='responder-pedido'),
]