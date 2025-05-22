# jogo/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from protocolos.models import User  # Mude esta importação

class CadastroForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User  # Mude para o modelo User de protocolos
        fields = ('username', 'email', 'password1', 'password2')

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)