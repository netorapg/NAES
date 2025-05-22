import os
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CadastroForm, LoginForm
from protocolos.models import User

def sinuca(request):
    return render(request, 'jogo/sobre.html')

def sobre(request):
    project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    estrutura = []
    for root, dirs, files in os.walk(project_path):
        level = root.replace(project_path, '').count(os.sep)
        indent = ' ' * 4 * level
        estrutura.append(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            estrutura.append(f"{subindent}{f}")
    
    context = {
        'estrutura_projeto': '\n'.join(estrutura),
        'title': 'Sobre o Projeto'
    }
    return render(request, 'jogo/sobre.html', context)

def cadastro_view(request):
    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Autologin após cadastro
            return redirect('jogo:home')
    else:
        form = CadastroForm()
    return render(request, 'jogo/cadastro.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('jogo:sinuca')  # Mude para 'sinuca' em vez de 'jogo'
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('jogo:sinuca')  # Atualize aqui também
            else:
                messages.error(request, 'Usuário ou senha incorretos')
    else:
        form = LoginForm()
    
    return render(request, 'jogo/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('jogo:login')

@login_required(login_url='/login/')
def sinuca_view(request):
    return render(request, 'jogo/sinuca.html', {'user': request.user})

def perfil_view(request):
    if not request.user.is_authenticated:
        return redirect('jogo:login')
    return render(request, 'jogo/perfil.html', {'user': request.user})

def ranking_view(request):
    from protocolos.models import User
    usuarios = User.objects.order_by('-pontuacao_maxima')[:10]  # Exemplo com campo fictício
    return render(request, 'jogo/ranking.html', {'usuarios': usuarios})