from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from .models import Status
from django.urls import reverse_lazy

class HomeView(TemplateView):
    template_name = "core/home.html"
    

#----------------------CRUD de Status----------------------#

class StatusListView(ListView):
    model = Status 
    fields = ['nome']
    template_name = 'core/status_list.html'
    context_object_name = 'status_list'
    success_url = reverse_lazy('core:status-list')
    
class StatusCreateView(CreateView):
    model = Status
    fields = ['nome']
    template_name = 'core/formulario.html'
    success_url = reverse_lazy('core:status-list')
    
class StatusUpdateView(UpdateView):
    model = Status
    fields = ['nome']
    template_name = 'core/formulario.html'
    success_url = reverse_lazy('core:status-list')

class StatusDeleteView(DeleteView):
    model = Status
    template_name = 'core/form_excluir.html'
    success_url = reverse_lazy('core:status-list')
    
