# 🎌 Anime Calendar – Calendário de Animes

[![Deploy](https://img.shields.io/badge/Deploy-Railway-blueviolet)](https://projetocursoficdjango-production.up.railway.app/)
[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.2-green.svg)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-Educational-orange.svg)](LICENSE)

Uma plataforma web completa desenvolvida em **Django** para organizar, visualizar e interagir com animes por temporada. O sistema integra dados do **MyAnimeList** através da **Jikan API v4**, oferecendo uma experiência rica e visual com cards responsivos em Bootstrap.

## 🚀 [Acesse a Aplicação ao Vivo](https://projetocursoficdjango-production.up.railway.app/)

> Explore o projeto em produção hospedado no Railway! 🎉

---

## 📋 Índice

- [Funcionalidades](#-funcionalidades)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Arquitetura do Projeto](#-arquitetura-do-projeto)
- [Modelos do Banco de Dados](#-modelos-do-banco-de-dados)
- [Instalação e Configuração](#️-instalação-e-configuração-passo-a-passo)
- [Estrutura de Diretórios](#-estrutura-de-diretórios)
- [Funcionalidades Detalhadas](#-funcionalidades-detalhadas)
- [API Externa](#-api-externa-jikan)
- [Deploy](#-deploy)
- [Contribuindo](#-contribuindo)

---

## ✨ Funcionalidades

### 📺 Sistema de Animes
- **Listagem Completa** – Visualize todos os animes cadastrados no banco de dados
- **Busca e Filtros** – Pesquise por título, gênero, temporada e status
- **Temporadas Atuais** – Veja animes da temporada atual direto do MyAnimeList
- **Detalhes Completos** – Informações detalhadas incluindo sinopse, trailer, episódios e datas

### 👤 Sistema de Usuários
- **Autenticação Completa** – Registro, login, logout e recuperação de senha
- **Perfis Personalizados** – Cada usuário tem seu perfil customizável
- **Sistema VIP** – Usuários VIP podem fazer upload de avatares e banners personalizados
- **Avatares Padrão** – 7 avatares pré-definidos disponíveis para todos os usuários

### ⭐ Interatividade
- **Sistema de Favoritos** – Marque e organize seus animes favoritos
- **Comentários e Respostas** – Comente sobre animes e responda outros usuários
- **Likes em Comentários** – Sistema de curtidas para interação social
- **Edição e Exclusão** – Gerencie seus próprios comentários

### 🎨 Interface
- **Design Responsivo** – Interface adaptável para desktop, tablet e mobile
- **Bootstrap 5** – Design moderno e componentes profissionais
- **Cards Visuais** – Exibição em cards com imagens, informações e ações
- **Paginação** – Navegação fluida entre múltiplas páginas de conteúdo

---

## 🧩 Tecnologias Utilizadas

### Backend
- **Python 3.13+** – Linguagem de programação principal
- **Django 5.2** – Framework web full-stack
- **Django ORM** – Mapeamento objeto-relacional para banco de dados
- **SQLite** – Banco de dados (desenvolvimento) / PostgreSQL (produção)

### Frontend
- **HTML5 & CSS3** – Estrutura e estilização
- **Bootstrap 5** – Framework CSS responsivo
- **JavaScript** – Interatividade e dinamismo
- **Template Engine Django** – Sistema de templates com herança

### APIs e Integrações
- **Jikan API v4** – Wrapper público não-oficial para MyAnimeList
- **Deep Translator** – Tradução automática de sinopses (opcional)
- **Django Cache Framework** – Sistema de cache para otimização

### Deployment
- **Railway** – Plataforma de hospedagem
- **Gunicorn** – Servidor WSGI para produção
- **WhiteNoise** – Serviço de arquivos estáticos
- **PostgreSQL** – Banco de dados em produção

---

## 🏗️ Arquitetura do Projeto

O projeto segue a arquitetura **MTV (Model-Template-View)** do Django, organizado em apps modulares:

### Apps Principais

| App | Responsabilidade | Principais Modelos |
|-----|------------------|-------------------|
| **anime** | Gerenciamento de animes, temporadas e gêneros | `Anime`, `Temporada`, `Genero`, `Studio` |
| **core** | Funcionalidades centrais e sincronização | `AnimeSyncStatus`, `SyncLog`, `Favorito` |
| **comments** | Sistema completo de comentários | `Comentario`, `ComentarioLike` |
| **comentarios** | Extensão do sistema de comentários | Similar ao comments |
| **perfil** | Perfis de usuários e customização | `Perfil` |
| **users** | Autenticação e gerenciamento de usuários | Usa `User` do Django |
| **calendar_app** | Visualização em formato de calendário | (Em desenvolvimento) |
| **animecalendar** | Configurações principais do projeto | Settings, URLs, WSGI |

---

## 🗄️ Modelos do Banco de Dados

### 📺 App: `anime`

#### **Modelo `Anime`**
Armazena informações completas sobre cada anime.

```python
Campos principais:
- mal_id (int) – ID único do MyAnimeList
- titulo (str) – Título principal do anime
- titulo_ingles (str) – Título em inglês
- sinopse (text) – Descrição completa do anime
- imagem_url (url) – URL da imagem de capa
- trailer_url (url) – URL do trailer no YouTube
- tipo (choice) – TV, Filme, OVA ou Especial
- status (choice) – Em lançamento, Finalizado ou Pausado
- episodios_total (int) – Número total de episódios
- data_lancamento (date) – Data de início
- data_encerramento (date) – Data de término
- nota (float) – Avaliação do MyAnimeList
- popularidade (int) – Ranking de popularidade
```

**Relacionamentos:**
- `generos` → Many-to-Many com `Genero`
- `studios` → Many-to-Many com `Studio`
- `temporadas` → Many-to-Many com `Temporada`

---

#### **Modelo `Temporada`**
Define as temporadas do ano (inverno, primavera, verão, outono).

```python
Campos:
- ano (int) – Ano da temporada (ex: 2025)
- estacao (choice) – INVERNO, PRIMAVERA, VERAO, OUTONO
- data_inicio (date) – Data de início da temporada
- data_fim (date) – Data de término da temporada
- is_atual (bool) – Marca se é a temporada atual

Constraint: Combinação única de ano e estação
```

---

#### **Modelo `Genero`**
Categorias/gêneros de animes (Ação, Comédia, Drama, etc.).

```python
Campos:
- nome (str) – Nome do gênero (único)
- descricao (text) – Descrição opcional do gênero
```

---

#### **Modelo `Studio`**
Estúdios de animação responsáveis pela produção.

```python
Campos:
- nome (str) – Nome do estúdio (único)
- site_oficial (url) – Website oficial do estúdio
```

---

### 👤 App: `perfil`

#### **Modelo `Perfil`**
Extensão do modelo User do Django com customizações.

```python
Campos principais:
- user (OneToOne) – Relacionamento 1:1 com User
- avatar_choice (choice) – Seleção de 7 avatares padrão
- is_vip (bool) – Define se usuário tem privilégios VIP
- custom_avatar (str) – URL de avatar personalizado (apenas VIP)
- custom_banner (str) – URL de banner personalizado (apenas VIP)
- bio (text) – Biografia do usuário
- data_nascimento (date) – Data de nascimento
- localizacao (str) – Localização do usuário

Signals: Criado automaticamente quando User é criado
```

**Avatares disponíveis:**
- `avatar_1.jpg` até `avatar_7.jpg` – Avatares padrão para todos
- Upload customizado – Apenas para usuários VIP

---

### 💬 App: `comments`

#### **Modelo `Comentario`**
Sistema hierárquico de comentários com respostas.

```python
Campos:
- anime (ForeignKey) → Anime comentado
- user (ForeignKey) → Autor do comentário
- parent (ForeignKey) → Comentário pai (para respostas)
- texto (text) – Conteúdo do comentário
- created_at (datetime) – Data de criação
- updated_at (datetime) – Data da última edição
- is_editado (bool) – Marca se foi editado
- is_deletado (bool) – Soft delete (comentário removido)
- deletado_por_admin (bool) – Se foi removido por admin

Relacionamento: Suporta comentários aninhados (respostas)
```

---

#### **Modelo `ComentarioLike`**
Sistema de curtidas para comentários.

```python
Campos:
- comentario (ForeignKey) → Comentário curtido
- user (ForeignKey) → Usuário que curtiu
- created_at (datetime) – Data da curtida

Constraint: Um usuário só pode curtir uma vez o mesmo comentário
```

---

### 🌟 App: `core`

#### **Modelo `Favorito`**
Relacionamento entre usuários e seus animes favoritos.

```python
Campos:
- user (ForeignKey) → Usuário
- anime (ForeignKey) → Anime favoritado
- created_at (datetime) – Data que foi favoritado

Constraint: Um usuário não pode favoritar o mesmo anime duas vezes
```

---

#### **Modelo `AnimeSyncStatus`**
Controle de sincronização com a API externa.

```python
Campos:
- anime (OneToOne) → Anime sincronizado
- last_synced_at (datetime) – Última sincronização
- last_payload (json) – Dados da última sincronização
- etag (str) – Tag para controle de cache

Uso: Evita requisições desnecessárias à API
```

---

#### **Modelo `SyncLog`**
Log de operações de sincronização com MyAnimeList.

```python
Campos:
- tipo (choice) – FULL_IMPORT, ATUALIZAR_TEMPORADA, ATUALIZAR_ANIME
- source (choice) – MyAnimeList (MAL)
- status (choice) – SUCESSO ou ERRO
- temporada (ForeignKey) → Temporada sincronizada (opcional)
- anime (ForeignKey) → Anime sincronizado (opcional)
- mensagem (text) – Detalhes da operação
- created_at (datetime) – Data da operação
- detalhes (json) – Informações adicionais

Uso: Auditoria e debug de sincronizações
```

---

## 🛠️ Instalação e Configuração (Passo a Passo)

### 📋 Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- **Python 3.13+** → [Download Python](https://www.python.org/downloads/)
- **pip** (gerenciador de pacotes Python) → Vem com Python
- **Git** → [Download Git](https://git-scm.com/downloads)
- **Editor de código** → VS Code, PyCharm ou similar (opcional)

---

### 1️⃣ Clone o Repositório

Abra seu terminal e execute:

```bash
git clone https://github.com/LucasdevBastos/PROJETO_CURSO_FIC_DJANGO.git
cd PROJETO_CURSO_FIC_DJANGO
```

---

### 2️⃣ Crie um Ambiente Virtual

O ambiente virtual isola as dependências do projeto:

#### Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux/Mac:
```bash
python3 -m venv venv
source venv/bin/activate
```

**Você verá `(venv)` no início da linha do terminal quando ativado.**

---

### 3️⃣ Instale as Dependências

Com o ambiente virtual ativado, instale todas as bibliotecas necessárias:

```bash
pip install -r requirements.txt
```

**Principais dependências instaladas:**
- Django 5.2
- requests (para API)
- deep-translator (tradução)
- pillow (processamento de imagens)
- gunicorn (servidor produção)
- whitenoise (arquivos estáticos)

---

### 4️⃣ Configure o Banco de Dados

Execute as migrações para criar todas as tabelas:

```bash
python manage.py migrate
```

**O que acontece:**
- Cria o arquivo `db.sqlite3` (banco de dados)
- Cria todas as tabelas definidas nos modelos
- Aplica índices e constraints

**Saída esperada:**
```
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying anime.0001_initial... OK
  ...
```

---

### 5️⃣ Crie um Superusuário (Admin)

Para acessar o painel administrativo Django:

```bash
python manage.py createsuperuser
```

**Será solicitado:**
- Username (nome de usuário)
- Email (opcional, pode deixar em branco)
- Password (senha - não aparece enquanto digita)

**Exemplo:**
```
Username: admin
Email: admin@exemplo.com
Password: ********
Password (again): ********
Superuser created successfully.
```

---

### 6️⃣ Carregue Dados Iniciais (Opcional)

Se houver fixtures (dados iniciais), você pode carregá-los:

```bash
python manage.py loaddata avatars
```

---

### 7️⃣ Inicie o Servidor de Desenvolvimento

Agora é só rodar o servidor:

```bash
python manage.py runserver
```

**Servidor iniciado!** Você verá algo como:

```
Django version 5.2, using settings 'animecalendar.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

---

### 8️⃣ Acesse a Aplicação

Abra seu navegador e acesse:

- **Aplicação principal:** `http://localhost:8000`
- **Painel admin:** `http://localhost:8000/admin`
  - Login com o superusuário criado no passo 5

---

### 9️⃣ Comandos Úteis

#### Criar novas migrações (após alterar models.py):
```bash
python manage.py makemigrations
```

#### Aplicar migrações pendentes:
```bash
python manage.py migrate
```

#### Coletar arquivos estáticos (para produção):
```bash
python manage.py collectstatic
```

#### Criar um novo app:
```bash
python manage.py startapp nome_do_app
```

#### Executar testes:
```bash
python manage.py test
```

#### Abrir shell interativo do Django:
```bash
python manage.py shell
```

---

## 📁 Estrutura de Diretórios

```text
PROJETO_CURSO_FIC_DJANGO/
│
├── 📄 manage.py                    # Script principal do Django
├── 📄 db.sqlite3                   # Banco de dados SQLite (desenvolvimento)
├── 📄 requirements.txt             # Dependências Python do projeto
├── 📄 Procfile                     # Configuração Railway (deploy)
├── 📄 railway.json                 # Configuração Railway
├── 📄 railway_init.sh              # Script inicialização Railway
├── 📄 start.sh                     # Script de start do servidor
├── 📄 validate_deploy.sh           # Validação de deploy
├── 📄 manage_avatars.py            # Gerenciamento de avatares
│
├── 📁 animecalendar/               # Configurações principais do projeto
│   ├── __init__.py
│   ├── settings.py                 # Configurações globais do Django
│   ├── urls.py                     # URLs principais do projeto
│   ├── wsgi.py                     # Interface WSGI para servidores
│   ├── asgi.py                     # Interface ASGI (async)
│   ├── views.py                    # Views compartilhadas
│   └── templates/
│       ├── base.html               # Template base (herança)
│       └── landing.html            # Página inicial
│
├── 📁 anime/                       # App principal de animes
│   ├── models.py                   # Modelos: Anime, Temporada, Genero, Studio
│   ├── views.py                    # Views de listagem e busca
│   ├── urls.py                     # URLs do app anime
│   ├── admin.py                    # Configuração do Django Admin
│   ├── apps.py                     # Configuração do app
│   ├── tests.py                    # Testes unitários
│   ├── migrations/                 # Migrações do banco de dados
│   ├── management/                 # Comandos customizados
│   │   └── commands/
│   └── templates/
│       ├── anime_list.html         # Listagem de animes
│       ├── favoritos.html          # Animes favoritos do usuário
│       └── temporadas.html         # Animes por temporada
│
├── 📁 core/                        # Funcionalidades centrais
│   ├── models.py                   # Favorito, AnimeSyncStatus, SyncLog
│   ├── views.py                    # Views compartilhadas
│   ├── jikan_api.py                # Integração com Jikan API
│   ├── urls.py
│   ├── services/                   # Lógica de negócio
│   ├── migrations/
│   └── templates/
│       └── core/
│
├── 📁 comments/                    # Sistema de comentários
│   ├── models.py                   # Comentario, ComentarioLike
│   ├── views.py                    # CRUD de comentários
│   ├── urls.py
│   ├── admin.py
│   ├── migrations/
│   └── templates/
│
├── 📁 comentarios/                 # Extensão de comentários
│   ├── models.py
│   ├── views.py
│   ├── forms.py                    # Formulários Django
│   ├── urls.py
│   ├── migrations/
│   └── templates/
│       └── comentarios/
│
├── 📁 perfil/                      # Perfis de usuários
│   ├── models.py                   # Modelo Perfil
│   ├── views.py                    # Edição de perfil
│   ├── forms.py                    # Formulário de perfil
│   ├── urls.py
│   ├── admin.py
│   ├── migrations/
│   └── templates/
│       └── perfil/
│           ├── perfil_edit.html    # Editar perfil
│           └── perfil_view.html    # Ver perfil
│
├── 📁 users/                       # Gerenciamento de usuários
│   ├── models.py
│   ├── views.py                    # Login, registro, logout
│   ├── urls.py
│   ├── migrations/
│   └── templates/
│       └── users/
│
├── 📁 calendar_app/                # Visualização em calendário
│   ├── models.py
│   ├── views.py
│   ├── services.py                 # Lógica de calendário
│   ├── urls.py
│   └── templates/
│       └── calendar_app/
│
├── 📁 static/                      # Arquivos estáticos (CSS, JS, imagens)
│   ├── css/
│   │   ├── style.css               # Estilos customizados
│   │   └── pages/                  # CSS específicos de páginas
│   ├── js/
│   │   ├── loadCSS.js              # Carregamento assíncrono CSS
│   │   └── pages/                  # JS específicos de páginas
│   └── avatars/                    # Avatares padrão
│       ├── avatar_1.jpg
│       ├── avatar_2.jpg
│       └── ...
│
├── 📁 staticfiles/                 # Arquivos estáticos coletados (produção)
│   └── (gerado por collectstatic)
│
├── 📁 media/                       # Uploads de usuários
│   └── avatars/                    # Avatares customizados VIP
│       └── 2025/
│
├── 📁 templates/                   # Templates compartilhados
│   ├── includes/
│   │   └── avatar.html             # Componente de avatar
│   ├── registration/               # Templates de autenticação
│   │   ├── login.html
│   │   ├── register.html
│   │   └── password_reset.html
│   └── users/
│
└── 📁 logs/                        # Logs da aplicação
    └── (arquivos de log)
```

---

## 🎯 Funcionalidades Detalhadas

### 1. Sistema de Animes

#### **Listagem de Animes** (`anime/views.py`)
- **Função:** `anime_list(request)`
- **URL:** `/animes/`
- **Descrição:** Lista todos os animes com paginação, busca e filtros
- **Recursos:**
  - Busca por título (japonês ou inglês)
  - Filtro por temporada
  - Filtro por gênero
  - Filtro por status (lançamento, finalizado, pausado)
  - Paginação (20 animes por página)
  - Ordenação por popularidade ou nota

#### **Animes da Temporada** (`anime/views.py`)
- **Função:** `temporadas_view(request)`
- **URL:** `/animes/temporadas/`
- **Descrição:** Busca animes da temporada atual via Jikan API
- **Processo:**
  1. Identifica temporada atual (inverno/primavera/verão/outono)
  2. Consulta API do MyAnimeList via Jikan
  3. Cacheia resultados por 4 horas
  4. Traduz sinopses automaticamente (se disponível)
  5. Exibe em cards com imagem, título, sinopse e trailer

---

### 2. Integração com Jikan API

#### **Classe JikanAPI** (`core/jikan_api.py`)

**Métodos principais:**

```python
# Buscar anime por ID do MyAnimeList
JikanAPI.get_anime(mal_id)

# Buscar animes da temporada
JikanAPI.get_season_anime(year, season)

# Buscar temporada atual
JikanAPI.get_current_season()

# Buscar animes por título
JikanAPI.search_anime(query)

# Buscar top animes
JikanAPI.get_top_anime(type='tv', page=1)
```

**Recursos:**
- **Cache automático** (4 horas) para reduzir requisições
- **Timeout** de 5 segundos para evitar travamentos
- **Tratamento de erros** robusto
- **Rate limiting** respeitado (3 req/segundo na API)
- **Tradução automática** de sinopses com GoogleTranslator

**Exemplo de uso:**
```python
from core.jikan_api import JikanAPI

# Buscar animes do inverno de 2025
animes = JikanAPI.get_season_anime(2025, 'winter')

# Buscar detalhes de um anime específico
anime = JikanAPI.get_anime(52991)  # ID do MyAnimeList
```

---

### 3. Sistema de Favoritos

#### **Como funciona:**
1. Usuário clica no botão "Favoritar" em um anime
2. Sistema verifica se já não está favoritado
3. Cria registro na tabela `Favorito`
4. Atualiza interface em tempo real (AJAX)

#### **Views relacionadas:**
- `adicionar_favorito(request, anime_id)` → POST
- `remover_favorito(request, anime_id)` → POST
- `listar_favoritos(request)` → GET

**Template:** `anime/favoritos.html`

---

### 4. Sistema de Comentários

#### **Funcionalidades:**
- ✍️ Criar comentário em um anime
- 💬 Responder comentários (thread aninhada)
- ✏️ Editar próprios comentários
- 🗑️ Excluir próprios comentários (soft delete)
- 👍 Curtir comentários de outros usuários
- 👮 Moderação por admins

#### **Views principais:**
- `criar_comentario(request, anime_id)`
- `editar_comentario(request, comentario_id)`
- `excluir_comentario(request, comentario_id)`
- `curtir_comentario(request, comentario_id)`
- `responder_comentario(request, comentario_id)`

**Soft Delete:** Comentários "excluídos" não são removidos do banco, apenas marcados como `is_deletado=True` para preservar thread.

---

### 5. Sistema de Perfis

#### **Funcionalidades:**
- 👤 Perfil criado automaticamente ao registrar
- 🖼️ Escolha de 7 avatares padrão
- ⭐ Usuários VIP podem fazer upload de avatar customizado
- 📝 Biografia e informações pessoais
- 📅 Data de nascimento
- 📍 Localização

#### **Views:**
- `perfil_view(request, username)` → Visualizar perfil público
- `perfil_edit(request)` → Editar próprio perfil

**Template:** `perfil/perfil_edit.html`

**Signal:** Perfil criado automaticamente via `post_save` do User.

---

### 6. Sistema de Autenticação

#### **Rotas disponíveis:**
- `/login/` → Login de usuário
- `/register/` → Registro de novo usuário
- `/logout/` → Logout
- `/password-reset/` → Recuperação de senha
- `/password-change/` → Alteração de senha

**Usa:** Django Authentication System (builtin)

---

## 🔌 API Externa: Jikan

### O que é Jikan?

**Jikan** é uma API REST não-oficial e gratuita que fornece acesso aos dados do **MyAnimeList** (maior banco de dados de animes do mundo).

### Documentação Oficial
📖 [https://docs.api.jikan.moe/](https://docs.api.jikan.moe/)

### Endpoints utilizados no projeto:

| Endpoint | Descrição | Uso no Projeto |
|----------|-----------|----------------|
| `/anime/{id}` | Detalhes de um anime específico | Sincronização de dados |
| `/seasons/{year}/{season}` | Animes de uma temporada | Listagem de temporadas |
| `/seasons/now` | Animes da temporada atual | Página de temporadas |
| `/top/anime` | Top animes ranqueados | Descoberta de animes |
| `/anime?q={query}` | Busca de animes | Sistema de busca |

### Limitações da API:
- **Rate Limit:** 3 requisições por segundo, 60 por minuto
- **Cache recomendado:** Pelo menos 24 horas
- **Timeout:** Resposta pode demorar até 5 segundos
- **Disponibilidade:** ~99% uptime (serviço gratuito)

### Como o projeto lida com isso:
✅ **Cache de 4 horas** para todos os endpoints  
✅ **Timeout de 5 segundos** configurado  
✅ **Tratamento de erros** para falhas da API  
✅ **Fallback** para dados locais quando API falha  

---

## 🌐 Deploy

### Plataforma: Railway

O projeto está hospedado no **Railway**, uma plataforma moderna de deploy com:
- ✅ Deploy automático via Git
- ✅ PostgreSQL integrado
- ✅ SSL/HTTPS automático
- ✅ Variáveis de ambiente seguras
- ✅ Logs em tempo real

### 🔗 Link da Aplicação
**[https://projetocursoficdjango-production.up.railway.app/](https://projetocursoficdjango-production.up.railway.app/)**

---

### Arquivos de Configuração

#### **Procfile**
Define o comando para iniciar o servidor em produção:
```
web: gunicorn animecalendar.wsgi --log-file -
```

#### **railway.json**
Configurações específicas do Railway:
```json
{
  "builder": "nixpacks",
  "build": {
    "command": "python manage.py migrate && python manage.py collectstatic --noinput"
  }
}
```

#### **railway_init.sh**
Script executado antes do deploy:
- Instala dependências
- Executa migrações
- Coleta arquivos estáticos

#### **start.sh**
Script de inicialização do servidor:
- Configura variáveis de ambiente
- Inicia Gunicorn com workers otimizados

#### **validate_deploy.sh**
Script de validação pós-deploy:
- Verifica conectividade do banco
- Testa endpoints principais
- Valida arquivos estáticos

---

### Variáveis de Ambiente (Produção)

```bash
SECRET_KEY=<chave-secreta-django>
DEBUG=False
ALLOWED_HOSTS=projetocursoficdjango-production.up.railway.app
DATABASE_URL=<url-postgresql-railway>
DISABLE_COLLECTSTATIC=0
```

---

### Como fazer deploy:

1. **Conecte ao Railway**
   - Crie conta em [railway.app](https://railway.app)
   - Conecte seu repositório GitHub

2. **Configure variáveis de ambiente**
   - Adicione `SECRET_KEY`, `DEBUG`, etc.

3. **Deploy automático**
   - Cada push na branch configurada faz deploy automático

4. **Monitore**
   - Veja logs em tempo real no painel Railway
   - Configure alertas para erros

---

## 🤝 Contribuindo

Contribuições são muito bem-vindas! Siga estes passos:

### 1. Fork o Projeto
Clique em "Fork" no topo do repositório GitHub.

### 2. Clone seu Fork
```bash
git clone https://github.com/SEU-USUARIO/PROJETO_CURSO_FIC_DJANGO.git
cd PROJETO_CURSO_FIC_DJANGO
```

### 3. Crie uma Branch
```bash
git checkout -b feature/MinhaNovaFuncionalidade
```

**Convenção de nomes:**
- `feature/` → Nova funcionalidade
- `fix/` → Correção de bug
- `docs/` → Documentação
- `refactor/` → Refatoração de código

### 4. Faça suas Alterações
Desenvolva sua funcionalidade ou correção.

### 5. Commit suas Mudanças
```bash
git add .
git commit -m "feat: Adiciona sistema de notificações"
```

**Convenção de commits:**
- `feat:` → Nova funcionalidade
- `fix:` → Correção de bug
- `docs:` → Documentação
- `style:` → Formatação
- `refactor:` → Refatoração
- `test:` → Testes

### 6. Push para o GitHub
```bash
git push origin feature/MinhaNovaFuncionalidade
```

### 7. Abra um Pull Request
- Acesse seu fork no GitHub
- Clique em "Compare & pull request"
- Descreva suas alterações detalhadamente
- Aguarde review

---

### Diretrizes de Contribuição

#### Código
- ✅ Siga PEP 8 (estilo Python)
- ✅ Adicione docstrings em funções
- ✅ Comente código complexo
- ✅ Mantenha funções pequenas e focadas

#### Testes
- ✅ Adicione testes para novas funcionalidades
- ✅ Garanta que todos os testes passam
```bash
python manage.py test
```

#### Documentação
- ✅ Atualize README quando necessário
- ✅ Documente novas APIs/endpoints
- ✅ Adicione comentários em código não-óbvio

---

## 📝 Licença

Este projeto foi desenvolvido para fins **educacionais** como parte do **Curso FIC**.

É livre para uso em projetos pessoais e educacionais. Para uso comercial, entre em contato com o autor.

---

## 👨‍💻 Autor

**Lucas Bastos**

- 🐙 GitHub: [@LucasdevBastos](https://github.com/LucasdevBastos)
- 📧 Email: Disponível no perfil do GitHub
- 💼 LinkedIn: [Conecte-se](https://linkedin.com)

---

## 📧 Contato e Suporte

### Encontrou um bug?
Abra uma [Issue no GitHub](https://github.com/LucasdevBastos/PROJETO_CURSO_FIC_DJANGO/issues) descrevendo:
- O que você esperava que acontecesse
- O que realmente aconteceu
- Passos para reproduzir o erro
- Screenshots (se aplicável)

### Tem uma sugestão?
Abra uma [Issue](https://github.com/LucasdevBastos/PROJETO_CURSO_FIC_DJANGO/issues) com a tag `enhancement` ou envie um Pull Request!

### Dúvidas?
- 💬 Abra uma [Discussion](https://github.com/LucasdevBastos/PROJETO_CURSO_FIC_DJANGO/discussions)
- 📧 Entre em contato via GitHub

---

## 🙏 Agradecimentos

- **MyAnimeList** – Pela fonte de dados de animes
- **Jikan API** – Pela API gratuita e bem documentada
- **Railway** – Pelo hosting gratuito e simples
- **Django Community** – Pelo framework incrível
- **Bootstrap** – Pelo framework CSS responsivo
- **Comunidade Open Source** – Por todas as bibliotecas utilizadas

---

## 📚 Recursos Adicionais

### Documentação Útil
- [Django Docs](https://docs.djangoproject.com/)
- [Jikan API Docs](https://docs.api.jikan.moe/)
- [Bootstrap 5 Docs](https://getbootstrap.com/docs/5.0/)
- [Railway Docs](https://docs.railway.app/)

### Tutoriais Relacionados
- [Django Girls Tutorial](https://tutorial.djangogirls.org/)
- [Real Python Django](https://realpython.com/tutorials/django/)
- [Django REST Framework](https://www.django-rest-framework.org/)

---

## 🗺️ Roadmap (Futuras Implementações)

### Em Desenvolvimento
- [ ] Sistema de notificações em tempo real
- [ ] Integração com Discord (bot de notificações)
- [ ] Sistema de badges e conquistas
- [ ] Recomendações personalizadas de animes

### Planejado
- [ ] API REST própria para mobile
- [ ] App mobile com React Native
- [ ] Sistema de listas personalizadas
- [ ] Calendário interativo de lançamentos
- [ ] Sistema de reviews e avaliações
- [ ] Integração com outras APIs (AniList, Kitsu)
- [ ] Dark mode
- [ ] PWA (Progressive Web App)

### Ideias Futuras
- [ ] Sistema de amizades e rede social
- [ ] Watch parties (assistir juntos)
- [ ] Integração com streaming (Crunchyroll, Netflix)
- [ ] Machine Learning para recomendações
- [ ] Análise de sentimento em comentários

---

<div align="center">

## ⭐ Se este projeto foi útil, considere dar uma estrela!

**Desenvolvido com ❤️ e Django**

---

### [⬆ Voltar ao topo](#-anime-calendar--calendário-de-animes)

</div>
