# MSN Clone - Sistema de Chat em Tempo Real

## 📋 Sobre o Projeto

O MSN Clone é uma aplicação web moderna desenvolvida em Django que replica as funcionalidades clássicas do MSN Messenger. O sistema implementa um chat em tempo real com recursos avançados de gerenciamento de amizades, status online/offline e interface responsiva.

## 🚀 Funcionalidades

### ✅ Implementadas

- **Autenticação de Usuários**
  - Sistema de registro e login
  - Gerenciamento de sessões
  - Middleware de atividade

- **Sistema de Amizades**
  - Envio de solicitações de amizade
  - Aceitar/recusar pedidos
  - Gerenciamento de contatos

- **Chat em Tempo Real**
  - Mensagens instantâneas via AJAX
  - Polling automático (2 segundos)
  - Interface não-bloqueante

- **Status de Usuários**
  - Indicadores online/offline
  - Rastreamento de última atividade
  - Atualização automática via middleware

- **Interface Responsiva**
  - Design Bootstrap 5
  - Ícones FontAwesome
  - Experiência mobile-friendly

## 🛠 Stack Tecnológico

### Backend
- **Django 5.x** - Framework web
- **SQLite** - Banco de dados
- **Python 3.13** - Linguagem de programação
- **Middleware Personalizado** - Controle de atividade

### Frontend
- **Bootstrap 5** - Framework CSS
- **JavaScript/AJAX** - Interatividade
- **FontAwesome** - Ícones
- **HTML5/CSS3** - Estrutura e estilo

## 🏗 Arquitetura do Sistema

### Estrutura de Apps
```
msnclone/
├── core/           # App principal com funcionalidades do chat
├── usuarios/       # App de autenticação
├── templates/      # Templates HTML
├── static/         # Arquivos estáticos
└── media/         # Upload de arquivos
```

### Modelos Principais

- **Perfil**: Extensão do User do Django com controle de atividade
- **Contato**: Gerenciamento de relacionamentos entre usuários
- **Conversa**: Agregador de mensagens entre usuários
- **Mensagem**: Conteúdo das conversas
- **Status**: Estados dos usuários
- **Emoticon**: Recursos de expressão

## 📊 Documentação Técnica

### Diagramas UML

O projeto inclui documentação completa em PlantUML:

1. **Diagrama de Casos de Uso** (`uso_caso_msn.puml`)
   - Atores do sistema
   - Funcionalidades principais
   - Fluxos de interação

2. **Diagrama de Classes** (`diagrama_classes_msn.puml`)
   - Estrutura de models
   - Relacionamentos
   - Views e middleware

### Gerando Diagramas

```bash
# Executar script automatizado
./gerar_diagramas.sh

# Ou manualmente com PlantUML
java -jar plantuml.jar -tpng uso_caso_msn.puml
java -jar plantuml.jar -tpng diagrama_classes_msn.puml
```

### Visualização Online
Acesse [PlantUML Online](http://www.plantuml.com/plantuml/uml/) e cole o conteúdo dos arquivos `.puml`.

## 🚀 Instalação e Execução

### Pré-requisitos
- Python 3.8+
- pip
- virtualenv (recomendado)

### Configuração do Ambiente

1. **Clone o repositório**
```bash
git clone <repository-url>
cd MSNCLONE/msnclone
```

2. **Crie e ative o ambiente virtual**
```bash
python -m venv msnc
source msnc/bin/activate  # Linux/Mac
# msnc\Scripts\activate   # Windows
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Configure o banco de dados**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Crie um superusuário**
```bash
python manage.py createsuperuser
```

6. **Colete arquivos estáticos**
```bash
python manage.py collectstatic
```

7. **Execute o servidor**
```bash
python manage.py runserver
```

## 🔧 Configuração

### Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto:

```env
SECRET_KEY=sua-secret-key-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Settings Importantes

- **MIDDLEWARE**: Inclui `UsuarioOnlineMiddleware` para rastreamento
- **STATIC_URL**: Configurado para servir arquivos estáticos
- **LOGIN_URL**: Redirecionamento para autenticação

## 📱 Como Usar

### Para Usuários

1. **Registro**: Crie uma conta na página de registro
2. **Login**: Acesse com suas credenciais
3. **Encontrar Amigos**: Navegue pela lista de usuários
4. **Adicionar Contatos**: Envie solicitações de amizade
5. **Chat**: Inicie conversas com seus contatos

### Funcionalidades do Chat

- **Mensagens em Tempo Real**: Atualizações automáticas a cada 2 segundos
- **Status Visual**: Indicadores online/offline em tempo real
- **Interface Intuitiva**: Design similar ao MSN clássico

## 🧪 Testes

```bash
# Executar todos os testes
python manage.py test

# Testes específicos de uma app
python manage.py test core
python manage.py test usuarios
```

## 📈 Monitoramento

### Logs
O sistema registra automaticamente:
- Atividade dos usuários
- Erros de aplicação
- Acessos e autenticação

### Performance
- Polling AJAX otimizado
- Queries de banco eficientes
- Cache de sessão ativado

## 🔒 Segurança

### Medidas Implementadas
- Proteção CSRF habilitada
- Autenticação obrigatória para funcionalidades principais
- Validação de formulários
- Sanitização de dados de entrada

## 🚀 Deployment

### Configurações de Produção

1. **Configure DEBUG=False**
2. **Defina ALLOWED_HOSTS adequadamente**
3. **Use banco de dados PostgreSQL/MySQL**
4. **Configure servidor web (nginx/Apache)**
5. **Implemente HTTPS**

### Docker (Opcional)

```dockerfile
# Dockerfile incluído no projeto
docker build -t msnclone .
docker run -p 8000:8000 msnclone
```

## 📚 API Endpoints

### Principais URLs

- `/` - Homepage
- `/usuarios/` - Lista de usuários
- `/chat/<id>/` - Interface de chat
- `/api/mensagens/` - Endpoint AJAX para mensagens
- `/documentacao/` - Documentação técnica

## 🤝 Contribuição

### Como Contribuir

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

### Guidelines

- Siga o padrão PEP 8 para Python
- Documente novas funcionalidades
- Inclua testes para código novo
- Mantenha a compatibilidade com versões anteriores

## 📞 Suporte

### Problemas Comuns

**Erro de Migração**
```bash
python manage.py migrate --fake-initial
```

**Arquivos Estáticos não Carregam**
```bash
python manage.py collectstatic --clear
```

**Problema de Permissões**
```bash
chmod +x gerar_diagramas.sh
```

## 📝 Changelog

### v1.0.0
- Sistema de autenticação completo
- Chat em tempo real via AJAX
- Gerenciamento de amizades
- Status online/offline
- Interface responsiva
- Documentação técnica completa

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👥 Autores

- **Desenvolvedor Principal** - Implementação completa do sistema

## 🎯 Roadmap

### Próximas Funcionalidades
- [ ] WebSocket para chat real-time
- [ ] Suporte a emoticons personalizados
- [ ] Chat em grupo
- [ ] Notificações push
- [ ] Histórico de mensagens
- [ ] Upload de arquivos
- [ ] Videochamadas (futuro)

## 📊 Estatísticas do Projeto

- **6 Models** Django
- **15+ Views** implementadas
- **20+ Templates** responsivos
- **2 Apps** principais
- **100% Funcional** - Todas as funcionalidades testadas

---

**MSN Clone** - Revivendo a experiência clássica do MSN Messenger com tecnologias modernas! 🚀
