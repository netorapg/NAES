# msnclone/core/urls.py
from django.urls import path
from .views import HomeView

# Boa prática para organizar as URLs do app
app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
]