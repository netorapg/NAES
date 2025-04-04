from django.shortcuts import render

def sinuca(request):
    return render(request, 'jogo/sinuca.html')