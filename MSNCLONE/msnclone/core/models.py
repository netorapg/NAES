from django.db import models
from django.contrib.auth.models import User

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
    # O status atual do usuário, relacionado à classe Status
    status_atual = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True, blank=True)
    frase = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return self.usuario.username


class Contato(models.Model):
    # O usuário que adiciona o contato
    usuario_principal = models.ForeignKey(User, related_name='contatos_adicionados', on_delete=models.CASCADE)
    # O amigo que foi adicionado
    amigo = models.ForeignKey(User, related_name='amigos_de', on_delete=models.CASCADE)
    data_amizade = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario_principal.username} -> {self.amigo.username}"


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