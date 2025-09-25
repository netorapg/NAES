from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UsuarioCreationForm(UserCreationForm):
    
    telefone = forms.CharField(label='Telefone', max_length=15, required=False)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'telefone']