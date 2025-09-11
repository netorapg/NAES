import django_filters
from django.contrib.auth.models import User

class UserFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(lookup_expr='icontains', label='Nome de usuário')
    
    class Meta:
        model = User
        fields = ['username', ]