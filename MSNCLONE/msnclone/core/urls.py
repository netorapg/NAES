# msnclone/core/urls.py
from django.urls import path
from .views import HomeView, StatusListView, StatusCreateView, StatusUpdateView, StatusDeleteView

app_name = 'core'

urlpatterns = [
    # URL da Home
    path('', HomeView.as_view(), name='home'),

    # URLs do CRUD de Status
    path('status/', StatusListView.as_view(), name='status-list'),
    path('status/cadastrar/', StatusCreateView.as_view(), name='status-create'),
    path('status/editar/<int:pk>/', StatusUpdateView.as_view(), name='status-update'),
    path('status/excluir/<int:pk>/', StatusDeleteView.as_view(), name='status-delete'),
]