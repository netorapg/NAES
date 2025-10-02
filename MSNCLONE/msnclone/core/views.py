from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import models
from django.db.models import Q
from django.http import JsonResponse
from .models import Contato, Status, Conversa, Mensagem, Perfil
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .filters import UserFilter

class HomeView(TemplateView):
    template_name = "core/home.html"

class DocumentacaoView(TemplateView):
    template_name = "core/documentacao.html"

class PlantUMLCodigoView(TemplateView):
    template_name = "core/plantuml_codigo.html"
    
class EnviarPedidoAmizadeView(LoginRequiredMixin, View):
    def post(self, request, pk):
        # Pega o usuário que vai receber o pedido
        receptor = get_object_or_404(User, pk=pk)
        # Pega o usuário que está enviando o pedido (o que está logado)
        solicitante = request.user

        # Lógica para evitar pedidos duplicados ou adicionar a si mesmo
        if receptor != solicitante:
            # Verifica se já existe um pedido
            contato, criado = Contato.objects.get_or_create(solicitante=solicitante, receptor=receptor)
            
            if criado:
                messages.success(request, f'Pedido de amizade enviado para {receptor.username}!')
            else:
                if contato.status == 'pendente':
                    messages.info(request, f'Você já enviou um pedido para {receptor.username}.')
                elif contato.status == 'aceito':
                    messages.info(request, f'Você já é amigo de {receptor.username}.')
                else:
                    messages.warning(request, f'Houve um problema com o pedido para {receptor.username}.')
        else:
            messages.error(request, 'Você não pode adicionar a si mesmo!')

        # Redireciona de volta para a lista de usuários
        return redirect('core:user-list')



class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'core/user_list.html'
    context_object_name = 'users'
    filterset_class = UserFilter
    paginate_by = 10  # ADICIONAR PAGINAÇÃO - 10 usuários por página
    
    def get_queryset(self):
        # OTIMIZADO: select_related para perfis se necessário
        queryset = User.objects.exclude(id=self.request.user.id).select_related('perfil')
        
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        
        return self.filterset.qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        return context

class MeusContatosView(LoginRequiredMixin, TemplateView):
    template_name = 'core/meus_contatos.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # OTIMIZADO: select_related evita N+1 queries
        # Cada contato já vem com os dados do receptor e solicitante carregados
        context['pedidos_enviados'] = Contato.objects.select_related('receptor', 'solicitante').filter(solicitante=user)
        
        context['pedidos_recebidos'] = Contato.objects.select_related('receptor', 'solicitante').filter(receptor=user)
        
        context['amigos'] = Contato.objects.select_related('receptor', 'solicitante').filter(
            Q(solicitante=user) | Q(receptor=user),
            status='aceito'
        )
        
        return context

class ResponderPedidoAmizadeView(LoginRequiredMixin, View):
    def post(self, request, pk):
        # Pega o contato/pedido específico
        contato = get_object_or_404(Contato, pk=pk, receptor=request.user)
        
        # Verifica a ação (aceitar ou recusar)
        acao = request.POST.get('acao')
        
        if acao == 'aceitar':
            contato.status = 'aceito'
            contato.save()
            messages.success(request, f'Você aceitou o pedido de {contato.solicitante.username}!')
        elif acao == 'recusar':
            contato.status = 'recusado'
            contato.save()
            messages.info(request, f'Você recusou o pedido de {contato.solicitante.username}.')
        
        return redirect('core:meus-contatos')


class ListarConversasView(LoginRequiredMixin, ListView):
    template_name = 'core/conversas_list.html'
    context_object_name = 'conversas'
    paginate_by = 5  # ADICIONAR PAGINAÇÃO - 5 conversas por página
    
    def get_queryset(self):
        # OTIMIZADO: prefetch_related para participantes
        return Conversa.objects.prefetch_related('participantes').filter(
            participantes=self.request.user
        ).order_by('-data_criacao')

class IniciarChatView(LoginRequiredMixin, View):
    def get(self, request, amigo_id):
        amigo = get_object_or_404(User, pk=amigo_id)
        
        # Verificar se são amigos
        amizade_existe = Contato.objects.filter(
            Q(solicitante=request.user, receptor=amigo, status='aceito') |
            Q(solicitante=amigo, receptor=request.user, status='aceito')
        ).exists()
        
        if not amizade_existe:
            messages.error(request, 'Você só pode conversar com seus amigos!')
            return redirect('core:meus-contatos')
        
        contato = Contato.objects.filter(
            Q(solicitante=request.user, receptor=amigo, status='aceito') |
            Q(solicitante=amigo, receptor=request.user, status='aceito')
        ).first()
        
        if contato and amigo in contato.bloqueado_por.all():
            messages.error(request, "Você não pode iniciar um chat com este usuário.")
            return redirect('core:meus-contatos')
        
        # Buscar conversa existente ou criar nova
        conversa = Conversa.objects.filter(participantes__in=[request.user]).\
                   filter(participantes__in=[amigo]).first()
        
        if not conversa:
            conversa = Conversa.objects.create()
            conversa.participantes.add(request.user, amigo)
        
        return redirect('core:chat', conversa_id=conversa.pk)


class ChatView(LoginRequiredMixin, TemplateView):
    template_name = 'core/chat.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        conversa_id = self.kwargs['conversa_id']
        
        # OTIMIZADO: select_related para evitar queries nas mensagens
        conversa = get_object_or_404(
            Conversa.objects.prefetch_related('participantes'), 
            pk=conversa_id, 
            participantes=self.request.user
        )
        
        # Pegar o outro participante
        outro_usuario = conversa.participantes.exclude(pk=self.request.user.pk).first()
        
        context['conversa'] = conversa
        context['outro_usuario'] = outro_usuario
        
        # CRÍTICO: select_related('remetente') evita 1 query por mensagem!
        context['mensagens'] = conversa.mensagem_set.select_related('remetente').all().order_by('data_envio')
        
        return context


class EnviarMensagemView(LoginRequiredMixin, View):
    def post(self, request, conversa_id):
        conversa = get_object_or_404(Conversa, pk=conversa_id, participantes=request.user)
        conteudo = request.POST.get('conteudo', '').strip()
        
        if conteudo:
            Mensagem.objects.create(
                conversa=conversa,
                remetente=request.user,
                conteudo=conteudo
            )
            messages.success(request, 'Mensagem enviada!')
        
        return redirect('core:chat', conversa_id=conversa_id)


class BuscarNovasMensagensView(LoginRequiredMixin, View):
    def get(self, request, conversa_id):
        conversa = get_object_or_404(Conversa, pk=conversa_id, participantes=request.user)
        
        try:
            ultima_mensagem_id = int(request.GET.get('ultima_mensagem_id', 0))
        except (ValueError, TypeError):
            ultima_mensagem_id = 0
        
        # OTIMIZADO: select_related('remetente') para evitar N+1
        novas_mensagens = Mensagem.objects.select_related('remetente').filter(
            conversa=conversa,
            id__gt=ultima_mensagem_id
        ).order_by('data_envio')
        
        mensagens_data = []
        for mensagem in novas_mensagens:
            mensagens_data.append({
                'id': mensagem.id,
                'conteudo': mensagem.conteudo,
                'remetente': mensagem.remetente.username,
                'remetente_id': mensagem.remetente.id,  # ADICIONAR para o JS
                'data_envio': mensagem.data_envio.strftime('%d/%m/%Y %H:%M'),
                'eh_minha': mensagem.remetente == request.user
            })
        
        return JsonResponse({
            'mensagens': mensagens_data,
            'success': True
        })


class EnviarMensagemAjaxView(LoginRequiredMixin, View):
    def post(self, request, conversa_id):
        conversa = get_object_or_404(Conversa, pk=conversa_id, participantes=request.user)
        conteudo = request.POST.get('conteudo', '').strip()
        
        if conteudo:
            mensagem = Mensagem.objects.create(
                conversa=conversa,
                remetente=request.user,
                conteudo=conteudo
            )
            
            return JsonResponse({
                'sucesso': True,
                'mensagem': {
                    'id': mensagem.id,
                    'conteudo': mensagem.conteudo,
                    'remetente': mensagem.remetente.username,
                    'remetente_id': mensagem.remetente.id,
                    'data_envio': mensagem.data_envio.strftime('%d/%m/%Y %H:%M'),
                    'timestamp': mensagem.data_envio.timestamp()
                }
            })
        
        return JsonResponse({'sucesso': False, 'erro': 'Mensagem vazia'})

@login_required
def excluir_amigo(request, contato_id):
    contato = get_object_or_404(Contato, id=contato_id)
    if (contato.solicitante == request.user or contato.receptor == request.user) and contato.status == 'aceito':
        contato.delete()
        messages.success(request, "Amizade excluída com sucesso.")
    else:
        messages.error(request, "Você não pode excluir esta amizade.")
    return redirect('core:meus-contatos')

@login_required
def bloquear_amigo(request, contato_id):
    contato = get_object_or_404(Contato, id=contato_id)
    if request.user in [contato.solicitante, contato.receptor]:
        contato.bloqueado_por.add(request.user)
        messages.success(request, "Usuário bloqueado.")
    else:
        messages.error(request, "Você não pode bloquear este usuário.")
    return redirect('core:meus-contatos')

@login_required
def desbloquear_amigo(request, contato_id):
    contato = get_object_or_404(Contato, id=contato_id)
    if request.user in contato.bloqueado_por.all():
        contato.bloqueado_por.remove(request.user)
        messages.success(request, "Usuário desbloqueado.")
    else:
        messages.error(request, "Você não pode desbloquear este usuário.")
    return redirect('core:meus-contatos')

@login_required
def editar_mensagem(request, mensagem_id):
    mensagem = get_object_or_404(Mensagem, id=mensagem_id, remetente=request.user)
    
    if request.method == 'POST':
        novo_conteudo = request.POST.get('conteudo', '').strip()
        if novo_conteudo:
            mensagem.conteudo = novo_conteudo
            mensagem.save()
            messages.success(request, "Mensagem editada com sucesso.")
        else:
            messages.error(request, "A mensagem não pode ficar vazia.")
        
        return redirect('core:chat', conversa_id=mensagem.conversa.id)
    
    # GET request - renderizar formulário de edição
    context = {
        'mensagem': mensagem,
        'conversa': mensagem.conversa
    }
    return render(request, 'core/editar_mensagem.html', context)

@login_required
def excluir_mensagem(request, mensagem_id):
    mensagem = get_object_or_404(Mensagem, id=mensagem_id, remetente=request.user)
    conversa_id = mensagem.conversa.id
    
    if request.method == 'POST':
        mensagem.delete()
        messages.success(request, "Mensagem excluída com sucesso.")
        return redirect('core:chat', conversa_id=conversa_id)
    
    # GET request - renderizar página de confirmação
    context = {
        'mensagem': mensagem,
        'conversa': mensagem.conversa
    }
    return render(request, 'core/confirmar_exclusao_mensagem.html', context)

# AJAX para editar mensagem
@login_required
def editar_mensagem_ajax(request, mensagem_id):
    if request.method == 'POST':
        mensagem = get_object_or_404(Mensagem, id=mensagem_id, remetente=request.user)
        novo_conteudo = request.POST.get('conteudo', '').strip()
        
        if novo_conteudo:
            mensagem.conteudo = novo_conteudo
            mensagem.save()
            
            return JsonResponse({
                'sucesso': True,
                'mensagem': {
                    'id': mensagem.id,
                    'conteudo': mensagem.conteudo,
                    'data_envio': mensagem.data_envio.strftime('%d/%m/%Y %H:%M'),
                }
            })
        else:
            return JsonResponse({'sucesso': False, 'erro': 'Mensagem não pode ficar vazia'})
    
    return JsonResponse({'sucesso': False, 'erro': 'Método não permitido'})

# AJAX para excluir mensagem
@login_required
def excluir_mensagem_ajax(request, mensagem_id):
    if request.method == 'POST':
        mensagem = get_object_or_404(Mensagem, id=mensagem_id, remetente=request.user)
        mensagem.delete()
        
        return JsonResponse({'sucesso': True})
    
    return JsonResponse({'sucesso': False, 'erro': 'Método não permitido'})


