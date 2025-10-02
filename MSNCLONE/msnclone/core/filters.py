import django_filters
from django.contrib.auth.models import User
from django import forms  # ADICIONAR ESTE IMPORT
from .models import Conversa

class UserFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(lookup_expr='icontains', label='Nome de usuário')
    
    class Meta:
        model = User
        fields = ['username']

class ConversaFilter(django_filters.FilterSet):
    # icontains - buscar por participante
    participante = django_filters.CharFilter(
        field_name='participantes__username', 
        lookup_expr='icontains',
        label='Buscar por participante'
    )
    
    # gte - conversas criadas a partir de uma data
    data_inicio = django_filters.DateFilter(
        field_name='data_criacao', 
        lookup_expr='gte',
        label='Criada a partir de',
        widget=forms.DateInput(attrs={'type': 'date'})  # CORREÇÃO: usar forms.DateInput
    )
    
    # lte - conversas criadas até uma data  
    data_fim = django_filters.DateFilter(
        field_name='data_criacao', 
        lookup_expr='lte',
        label='Criada até',
        widget=forms.DateInput(attrs={'type': 'date'})  # CORREÇÃO: usar forms.DateInput
    )
    
    class Meta:
        model = Conversa
        fields = ['participante', 'data_inicio', 'data_fim']