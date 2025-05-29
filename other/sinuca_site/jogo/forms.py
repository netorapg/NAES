# jogo/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from protocolos.models import User  # Mude esta importação

class CadastroForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User  # Mude para o modelo User de protocolos
        fields = ('username', 'email', 'password1', 'password2')

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'isHost', 'pontuacao_maxima')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'isHost', 'pontuacao_maxima', 'is_active', 'groups')


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)