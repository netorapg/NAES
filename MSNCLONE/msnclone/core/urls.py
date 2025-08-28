# msnclone/core/urls.py
from django.urls import path
from .views import (
    HomeView, UserListView, EnviarPedidoAmizadeView, MeusContatosView, ResponderPedidoAmizadeView,
    ListarConversasView, IniciarChatView, ChatView, EnviarMensagemView,
    BuscarNovasMensagensView, EnviarMensagemAjaxView, DocumentacaoView, PlantUMLCodigoView
)
from . import views

app_name = 'core'

urlpatterns = [
    # URL da Home
    path('', HomeView.as_view(), name='home'),
    
    # URLs de usuários e amizades
    path('usuarios/', UserListView.as_view(), name='user-list'),
    path('adicionar-amigo/<int:pk>/', EnviarPedidoAmizadeView.as_view(), name='adicionar-amigo'),
    path('meus-contatos/', MeusContatosView.as_view(), name='meus-contatos'),
    path('responder-pedido/<int:pk>/', ResponderPedidoAmizadeView.as_view(), name='responder-pedido'),
    path('excluir-amigo/<int:contato_id>/', views.excluir_amigo, name='excluir-amigo'),
    path('bloquear-amigo/<int:contato_id>/', views.bloquear_amigo, name='bloquear-amigo'),
    path('desbloquear-amigo/<int:contato_id>/', views.desbloquear_amigo, name='desbloquear-amigo'),
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
    
    # URLs para editar e excluir mensagens
    path('editar-mensagem/<int:mensagem_id>/', views.editar_mensagem, name='editar-mensagem'),
    path('excluir-mensagem/<int:mensagem_id>/', views.excluir_mensagem, name='excluir-mensagem'),
    
    # URLs AJAX para editar e excluir mensagens
    path('editar-mensagem-ajax/<int:mensagem_id>/', views.editar_mensagem_ajax, name='editar-mensagem-ajax'),
    path('excluir-mensagem-ajax/<int:mensagem_id>/', views.excluir_mensagem_ajax, name='excluir-mensagem-ajax'),
]