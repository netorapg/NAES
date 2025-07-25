from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import uuid
from django.utils import timezone


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    isOnline = models.BooleanField(default=False)

    # Adicione os related_name necessários
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='jogo_user_set',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='jogo_user_set',
        blank=True,
    )

    def __str__(self):
        return f"{self.username}"


class ChatMessage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room = models.CharField(max_length=100)  # Identificador da sala
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} ({self.room}): {self.message[:20]}"


class MesaSinuca(models.Model):
    STATUS_CHOICES = [
        ('disponivel', 'Disponível'),
        ('ocupada', 'Ocupada'),
        ('em_jogo', 'Em Jogo'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=100)
    criador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mesas_criadas')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='disponivel')
    max_jogadores = models.IntegerField(default=2)
    criada_em = models.DateTimeField(auto_now_add=True)
    jogadores = models.ManyToManyField(User, blank=True, related_name='mesas_participando')

    def pode_entrar(self, user):
        """Verifica se o usuário pode entrar na mesa"""
        return self.jogadores.count() < self.max_jogadores and self.status == 'disponivel'

    def entrar_mesa(self, user):
        """Adiciona jogador à mesa"""
        if self.pode_entrar(user):
            self.jogadores.add(user)
            if self.jogadores.count() == self.max_jogadores:
                self.status = 'em_jogo'
                self.save()
            return True
        return False

    def sair_mesa(self, user):
        """Remove jogador da mesa"""
        self.jogadores.remove(user)
        if self.jogadores.count() < self.max_jogadores:
            self.status = 'disponivel'
            self.save()

    def __str__(self):
        return f"{self.nome} - {self.get_status_display()}"
