# msnclone/core/urls.py
from django.urls import path
from .views import (
    HomeView, UserListView, EnviarPedidoAmizadeView, MeusContatosView, ResponderPedidoAmizadeView,
    ListarConversasView, IniciarChatView, ChatView, EnviarMensagemView,
    BuscarNovasMensagensView, EnviarMensagemAjaxView, DocumentacaoView, PlantUMLCodigoView
)
app_name = 'core'

urlpatterns = [
    # URL da Home
    path('', HomeView.as_view(), name='home'),
    
    # URLs de usuários e amizades
    path('usuarios/', UserListView.as_view(), name='user-list'),
    path('adicionar-amigo/<int:pk>/', EnviarPedidoAmizadeView.as_view(), name='adicionar-amigo'),
    path('meus-contatos/', MeusContatosView.as_view(), name='meus-contatos'),
    path('responder-pedido/<int:pk>/', ResponderPedidoAmizadeView.as_view(), name='responder-pedido'),
    
    # URLs do sistema de chat
    path('conversas/', ListarConversasView.as_view(), name='conversas'),
    path('iniciar-chat/<int:amigo_id>/', IniciarChatView.as_view(), name='iniciar-chat'),
    path('chat/<int:conversa_id>/', ChatView.as_view(), name='chat'),
    path('enviar-mensagem/<int:conversa_id>/', EnviarMensagemView.as_view(), name='enviar-mensagem'),
    
    # URLs AJAX para chat em tempo real
    path('buscar-mensagens/<int:conversa_id>/', BuscarNovasMensagensView.as_view(), name='buscar-mensagens'),
    path('enviar-mensagem-ajax/<int:conversa_id>/', EnviarMensagemAjaxView.as_view(), name='enviar-mensagem-ajax'),
    
    # Documentação
    path('documentacao/', DocumentacaoView.as_view(), name='documentacao'),
    path('plantuml-codigo/', PlantUMLCodigoView.as_view(), name='plantuml-codigo'),
]