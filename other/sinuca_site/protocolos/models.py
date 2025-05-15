from django.db import models


class User(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    lasLogin = models.DateTimeField(auto_now=True)
    isOnline = models.BooleanField(default=False)
    isHost = models.BooleanField(default=False)

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


