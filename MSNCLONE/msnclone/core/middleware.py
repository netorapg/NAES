from django.utils import timezone
from .models import Perfil

class UsuarioOnlineMiddleware:
    """
    Middleware para atualizar automaticamente a última atividade do usuário logado
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Atualizar atividade antes de processar a view
        if request.user.is_authenticated:
            try:
                perfil, created = Perfil.objects.get_or_create(usuario=request.user)
                perfil.atualizar_atividade()
            except Exception:
                # Se houver algum erro, continuar normalmente
                pass

        response = self.get_response(request)
        return response
