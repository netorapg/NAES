from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):  # Herda de AbstractUser ao invés de models.Model
    # Mantenha seus campos customizados
    created_at = models.DateTimeField(auto_now_add=True)
    lastLogin = models.DateTimeField(auto_now=True)
    isOnline = models.BooleanField(default=False)
    isHost = models.BooleanField(default=False)
    pontuacao_maxima = models.IntegerField(default=0)
    
    # Remova o campo password pois já vem do AbstractUser
    # Remova email pois já vem do AbstractUser
    
    # Adicione os related_name necessários
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='protocolos_user_set',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='protocolos_user_set',
        blank=True,
    )

    def __str__(self):
        return f"{self.username} ({self.email})"
class GameTable ( models.Model):
    TableType = models.ForeignKey('TableType', on_delete=models.CASCADE)
    table_number = models.IntegerField()
    status = models.CharField(max_length=20)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Table {self.table_number} - {self.TableType.table_type}"


class TableType(models.Model):
    table_type = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.table_type


class GameSession (models.Model):
    startTime = models.DateTimeField(auto_now_add=True)
    endTime = models.DateTimeField(auto_now=True)
    currentPlayer = models.ForeignKey(User, on_delete=models.CASCADE)
    scorePlayer1 = models.IntegerField()
    scorePlayer2 = models.IntegerField()

    def __str__(self):
        return f"Game Session {self.id} - Player: {self.currentPlayer.username}"


class ChatSystem(models.Model):
    messages = models.TextField()
    isActive = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Chat System - Active: {self.isActive}"


class Message(models.Model):
    content = models.TextField()
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=20)
    isPinned = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender.username} - Type: {self.type}"


class ModerationSystem(models.Model):
    mutedUsers = models.ManyToManyField(User, related_name='muted_users')
    
    def __str__(self):
        return f"Moderation System - Muted Users: {self.mutedUsers.count()}"


