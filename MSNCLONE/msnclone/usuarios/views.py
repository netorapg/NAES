from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import UsuarioCreationForm

class UsuarioCreateView(CreateView):
    form_class = UsuarioCreationForm
    template_name = 'usuarios/registro.html'
    success_url = reverse_lazy('usuarios:login')
