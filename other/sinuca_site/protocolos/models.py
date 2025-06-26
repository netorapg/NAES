from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
from django.utils import timezone

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    lastLogin = models.DateTimeField(auto_now=True)
    isOnline = models.BooleanField(default=False)
    isHost = models.BooleanField(default=False)
    
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

    def authenticate_user(self, password):
        """Autentica o usuário com a senha fornecida"""
        return self.check_password(password)
    
    def send_message(self, content, chat_system):
        """Envia uma mensagem para o sistema de chat"""
        return ChatMessage.objects.create(
            sender=self,
            content=content,
            chat_system=chat_system
        )

    def __str__(self):
        return f"{self.username} ({self.email})"


class TableType(models.Model):
    """Enum-like model para tipos de mesa"""
    POOL_8_BALL = 'pool_8'
    POOL_9_BALL = 'pool_9' 
    SNOOKER = 'snooker'
    
    TYPE_CHOICES = [
        (POOL_8_BALL, '8-Ball Pool'),
        (POOL_9_BALL, '9-Ball Pool'),
        (SNOOKER, 'Snooker'),
    ]
    
    name = models.CharField(max_length=20, choices=TYPE_CHOICES, unique=True)
    description = models.TextField()
    
    def __str__(self):
        return self.get_name_display()


class TableStatus(models.Model):
    """Enum-like model para status da mesa"""
    AVAILABLE = 'available'
    OCCUPIED = 'occupied'
    MAINTENANCE = 'maintenance'
    RESERVED = 'reserved'
    
    STATUS_CHOICES = [
        (AVAILABLE, 'Disponível'),
        (OCCUPIED, 'Ocupada'),
        (MAINTENANCE, 'Em Manutenção'),
        (RESERVED, 'Reservada'),
    ]
    
    name = models.CharField(max_length=20, choices=STATUS_CHOICES, unique=True)
    
    def __str__(self):
        return self.get_name_display()


class GameTable(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tableType = models.ForeignKey(TableType, on_delete=models.CASCADE)
    status = models.ForeignKey(TableStatus, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)
    players = models.ManyToManyField(User, blank=True, related_name='tables')
    
    def join_table(self, user):
        """Permite que um usuário se junte à mesa"""
        if self.players.count() < 2:
            self.players.add(user)
            if self.players.count() == 2:
                # Muda status para ocupada quando 2 jogadores se juntam
                occupied_status, _ = TableStatus.objects.get_or_create(name=TableStatus.OCCUPIED)
                self.status = occupied_status
                self.save()
            return True
        return False
    
    def start_game(self):
        """Inicia um jogo se há 2 jogadores"""
        if self.players.count() == 2:
            # Cria uma nova sessão de jogo
            players_list = list(self.players.all())
            session = GameSession.objects.create(
                table=self,
                player1=players_list[0],
                player2=players_list[1],
                currentPlayer=players_list[0]  # Primeiro jogador começa
            )
            return session
        return None

    def __str__(self):
        return f"Mesa {self.tableType} - {self.status}"


class GameSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    table = models.ForeignKey(GameTable, on_delete=models.CASCADE, related_name='sessions')
    startTime = models.DateTimeField(auto_now_add=True)
    endTime = models.DateTimeField(null=True, blank=True)
    player1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions_as_player1')
    player2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions_as_player2')
    currentPlayer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='current_sessions')
    scorePlayer1 = models.IntegerField(default=0)
    scorePlayer2 = models.IntegerField(default=0)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='won_sessions')
    
    def calculate_score(self):
        """Retorna um dicionário com as pontuações dos jogadores"""
        return {
            self.player1: self.scorePlayer1,
            self.player2: self.scorePlayer2
        }
    
    def end_game(self, winner_user):
        """Finaliza o jogo definindo o vencedor"""
        self.winner = winner_user
        self.endTime = timezone.now()
        self.save()
        
        # Libera a mesa
        available_status, _ = TableStatus.objects.get_or_create(name=TableStatus.AVAILABLE)
        self.table.status = available_status
        self.table.players.clear()
        self.table.save()

    def __str__(self):
        return f"Sessão {self.player1.username} vs {self.player2.username}"


class ModerationSystem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mutedUsers = models.ManyToManyField(User, blank=True, related_name='muted_in_systems')
    
    def filter_text(self, content):
        """Filtra texto com palavras proibidas (placeholder)"""
        # Implementar filtro de palavras ofensivas aqui
        forbidden_words = ['spam', 'hack', 'cheat']  # exemplo
        filtered_content = content
        for word in forbidden_words:
            filtered_content = filtered_content.replace(word, '*' * len(word))
        return filtered_content
    
    def mute_user(self, user, duration_minutes=60):
        """Silencia um usuário por um período determinado"""
        self.mutedUsers.add(user)
        # Aqui você poderia implementar um sistema de tempo de silenciamento
        return True
    
    def unmute_user(self, user):
        """Remove o silenciamento de um usuário"""
        self.mutedUsers.remove(user)

    def __str__(self):
        return f"Sistema de Moderação - {self.mutedUsers.count()} usuários silenciados"


class ChatSystem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    table = models.OneToOneField(GameTable, on_delete=models.CASCADE, related_name='chat_system')
    isActive = models.BooleanField(default=True)
    moderation = models.OneToOneField(ModerationSystem, on_delete=models.CASCADE, related_name='chat_system')
    
    def send_message(self, sender, content):
        """Envia uma mensagem se o usuário não estiver silenciado"""
        if sender not in self.moderation.mutedUsers.all():
            # Filtra o conteúdo
            filtered_content = self.moderation.filter_text(content)
            message = ChatMessage.objects.create(
                sender=sender,
                content=filtered_content,
                chat_system=self
            )
            return message
        return None
    
    def get_history(self, limit=50):
        """Retorna o histórico de mensagens"""
        return self.messages.order_by('-timestamp')[:limit]
    
    def clear_history(self):
        """Limpa o histórico de mensagens"""
        self.messages.all().delete()

    def __str__(self):
        return f"Chat da {self.table}"


class MessageType(models.Model):
    """Enum-like model para tipos de mensagem"""
    NORMAL = 'normal'
    SYSTEM = 'system'
    ANNOUNCEMENT = 'announcement'
    WARNING = 'warning'
    
    TYPE_CHOICES = [
        (NORMAL, 'Normal'),
        (SYSTEM, 'Sistema'),
        (ANNOUNCEMENT, 'Anúncio'),
        (WARNING, 'Aviso'),
    ]
    
    name = models.CharField(max_length=20, choices=TYPE_CHOICES, unique=True)
    
    def __str__(self):
        return self.get_name_display()


class ChatMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField()
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    timestamp = models.DateTimeField(auto_now_add=True)
    chat_system = models.ForeignKey(ChatSystem, on_delete=models.CASCADE, related_name='messages')
    type = models.ForeignKey(MessageType, on_delete=models.CASCADE)
    isPinned = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.sender.username}: {self.content[:50]}..."


