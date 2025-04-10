import os
from django.shortcuts import render

def sinuca(request):
    return render(request, 'jogo/sinuca.html')

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
    return render(request, 'jogo/sobre.html')