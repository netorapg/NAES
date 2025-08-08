from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

# Create your models here.

class Status(models.Model):
    nome = models.CharField(max_length=50, help_text="Ex: Online, Ausente, Ocupado")
    
    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = "Status"
        verbose_name_plural = "Status"


class Perfil(models.Model):
    # Um Perfil está associado a um único Usuário
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    frase = models.CharField(max_length=255, blank=True, null=True)
    ultima_atividade = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.usuario.username
    
    @property
    def esta_online(self):
        """Considera online se a última atividade foi nos últimos 5 minutos"""
        agora = timezone.now()
        limite = agora - timedelta(minutes=5)
        return self.ultima_atividade > limite
    
    @property
    def status_display(self):
        return "Online" if self.esta_online else "Offline"
    
    def atualizar_atividade(self):
        """Atualiza o timestamp da última atividade"""
        self.ultima_atividade = timezone.now()
        self.save(update_fields=['ultima_atividade'])


class Contato(models.Model):
    STATUS_CHOICES = (
        ('pendente', 'Pendente'),
        ('aceito', 'Aceito'),
        ('recusado', 'Recusado'),
    )
    
    solicitante = models.ForeignKey(User, related_name='pedidos_enviados', on_delete=models.CASCADE)
    receptor = models.ForeignKey(User, related_name='pedidos_recebidos', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pendente')
    data_solicitacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.solicitante} -> {self.receptor} ({self.status})"
    
    
class Conversa(models.Model):
    # Usuários que participam da conversa
    participantes = models.ManyToManyField(User, related_name='conversas')
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversa entre {', '.join([user.username for user in self.participantes.all()])}"


class Mensagem(models.Model):
    # A conversa a que esta mensagem pertence
    conversa = models.ForeignKey(Conversa, on_delete=models.CASCADE)
    # O usuário que enviou a mensagem
    remetente = models.ForeignKey(User, on_delete=models.CASCADE)
    conteudo = models.TextField()
    data_envio = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"De {self.remetente.username} em {self.data_envio.strftime('%d/%m/%Y %H:%M')}"


class Emoticon(models.Model):
    texto_atalho = models.CharField(max_length=10, help_text="Ex: :)")
    # O upload_to define um subdiretório dentro da pasta de media
    imagem_emoticon = models.ImageField(upload_to='emoticons/')

    def __str__(self):
        return self.texto_atalho