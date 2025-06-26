from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, MesaSinuca

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'isOnline', 'created_at', 'is_staff')
    list_filter = ('isOnline', 'is_staff', 'is_superuser', 'is_active', 'created_at')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-created_at',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Extras', {
            'fields': ('isOnline', 'created_at')
        }),
    )
    
    readonly_fields = ('created_at', 'id')

@admin.register(MesaSinuca)
class MesaSinucaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'criador', 'status', 'max_jogadores', 'count_jogadores', 'criada_em')
    list_filter = ('status', 'max_jogadores', 'criada_em')
    search_fields = ('nome', 'criador__username')
    readonly_fields = ('id', 'criada_em')
    ordering = ('-criada_em',)
    
    filter_horizontal = ('jogadores',)
    
    def count_jogadores(self, obj):
        return obj.jogadores.count()
    count_jogadores.short_description = 'Jogadores Atuais'
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'criador', 'status', 'max_jogadores')
        }),
        ('Jogadores', {
            'fields': ('jogadores',)
        }),
        ('Metadados', {
            'fields': ('id', 'criada_em'),
            'classes': ('collapse',)
        }),
    )
