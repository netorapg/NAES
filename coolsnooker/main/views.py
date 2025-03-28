from django.shortcuts import render

def home(request):
    return render(request, 'main/home.html')

def play(request):
    return render(request, 'main/play.html')

def about(request):
    return render(request, 'main/about.html')
