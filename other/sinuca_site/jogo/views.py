import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import CadastroForm, LoginForm
from .models import User, MesaSinuca

def home(request):
    """Página inicial - redireciona baseado na autenticação"""
    if request.user.is_authenticated:
        return redirect('jogo:sinuca')
    return render(request, 'jogo/sobre.html')

def sobre(request):
    """Página sobre o projeto"""
    return render(request, 'jogo/sobre.html')

def cadastro_view(request):
    """View para cadastro de usuários"""
    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('jogo:sinuca')
    else:
        form = CadastroForm()
    return render(request, 'jogo/cadastro.html', {'form': form})

def login_view(request):
    """View para login de usuários"""
    if request.user.is_authenticated:
        return redirect('jogo:sinuca')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, 'Login realizado com sucesso!')
                return redirect('jogo:sinuca')
            else:
                messages.error(request, 'Usuário ou senha incorretos')
    else:
        form = LoginForm()
    
    return render(request, 'jogo/login.html', {'form': form})

def logout_view(request):
    """View para logout"""
    logout(request)
    messages.info(request, 'Você foi desconectado.')
    return redirect('jogo:home')

@login_required(login_url='/login/')
def sinuca_view(request):
    """Tela principal do jogo com lista de mesas"""
    mesas = MesaSinuca.objects.all().order_by('-criada_em')
    minhas_mesas = mesas.filter(criador=request.user)
    outras_mesas = mesas.exclude(criador=request.user)
    
    # Adicionar informação se o usuário pode entrar em cada mesa
    for mesa in outras_mesas:
        mesa.usuario_pode_entrar = mesa.pode_entrar(request.user)
    
    context = {
        'user': request.user,
        'minhas_mesas': minhas_mesas,
        'outras_mesas': outras_mesas,
    }
    return render(request, 'jogo/sinuca.html', context)

@login_required
def criar_mesa(request):
    """View para criar uma nova mesa"""
    if request.method == 'POST':
        nome = request.POST.get('nome')
        max_jogadores = int(request.POST.get('max_jogadores', 2))
        
        mesa = MesaSinuca.objects.create(
            nome=nome,
            criador=request.user,
            max_jogadores=max_jogadores
        )
        
        # O criador automaticamente entra na mesa
        mesa.entrar_mesa(request.user)
        
        messages.success(request, f'Mesa "{nome}" criada com sucesso!')
        return redirect('jogo:sinuca')
    
    return render(request, 'jogo/criar_mesa.html')

@login_required
def entrar_mesa(request, mesa_id):
    """View para entrar em uma mesa"""
    mesa = get_object_or_404(MesaSinuca, id=mesa_id)
    
    if mesa.entrar_mesa(request.user):
        messages.success(request, f'Você entrou na mesa "{mesa.nome}"!')
        
        # Se a mesa estiver cheia, redireciona para o jogo
        if mesa.status == 'em_jogo':
            return redirect('jogo:jogar', mesa_id=mesa.id)
    else:
        messages.error(request, 'Não foi possível entrar na mesa.')
    
    return redirect('jogo:sinuca')

@login_required
def sair_mesa(request, mesa_id):
    """View para sair de uma mesa"""
    mesa = get_object_or_404(MesaSinuca, id=mesa_id)
    
    if request.user in mesa.jogadores.all():
        mesa.sair_mesa(request.user)
        messages.info(request, f'Você saiu da mesa "{mesa.nome}".')
    
    return redirect('jogo:sinuca')

@login_required
def excluir_mesa(request, mesa_id):
    """View para excluir uma mesa (apenas o criador pode)"""
    mesa = get_object_or_404(MesaSinuca, id=mesa_id)
    
    if mesa.criador == request.user:
        nome_mesa = mesa.nome
        mesa.delete()
        messages.success(request, f'Mesa "{nome_mesa}" excluída com sucesso!')
    else:
        messages.error(request, 'Você não tem permissão para excluir esta mesa.')
    
    return redirect('jogo:sinuca')

@login_required
def jogar(request, mesa_id):
    """Tela do jogo"""
    mesa = get_object_or_404(MesaSinuca, id=mesa_id)
    
    # Verifica se o usuário está na mesa
    if request.user not in mesa.jogadores.all():
        messages.error(request, 'Você não está nesta mesa.')
        return redirect('jogo:sinuca')
    
    # Supondo que exista um campo chamado chat_system na mesa
    chat_system = getattr(mesa, 'chat_system', None)
    
    context = {
        'mesa': mesa,
        'jogadores': mesa.jogadores.all(),
        'chat_system': chat_system,
    }
    return render(request, 'jogo/jogar.html', context)

def perfil_view(request):
    """View do perfil do usuário"""
    if not request.user.is_authenticated:
        return redirect('jogo:login')
    return render(request, 'jogo/perfil.html', {'user': request.user})

def ranking_view(request):
    """View do ranking de usuários"""
    usuarios = User.objects.all().order_by('username')
    return render(request, 'jogo/ranking.html', {'usuarios': usuarios})

# CRUD para User (apenas para administradores)
class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'
    paginate_by = 20
    ordering = ['username']

class UserCreateView(LoginRequiredMixin, CreateView):
    model = User
    fields = ['username', 'email', 'first_name', 'last_name']
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('jogo:user_list')

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['username', 'email', 'first_name', 'last_name', 'isOnline']
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('jogo:user_list')

class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('jogo:user_list')