# ================================
# DJANGO CHEATSHEET – COMANDOS
# ================================

# --- AMBIENTE VIRTUAL ---
# python3 -m venv venv
# Cria o ambiente virtual

# venv\Scripts\activate
# Ativa o venv no Windows

# source venv/bin/activate
# Ativa o venv no Linux/Mac

# deactivate
# Desativa o venv


# --- INSTALAÇÃO ---
# pip install django
# Instala o Django

# pip install django-environ
# Instala variável de ambiente


# --- INICIAR PROJETO ---
# django-admin startproject meu_projeto
# Cria o projeto

# django-admin startproject meu_projeto .
# Cria o projeto na pasta atual


# --- CRIAR APP ---
# python manage.py startapp meu_app
# Cria um novo app


# --- SERVIDOR ---
# python manage.py runserver
# Inicia servidor local

# python manage.py runserver 0.0.0.0:8000
# Inicia servidor aceitando conexões externas


# --- MIGRAÇÕES ---
# python manage.py makemigrations
# Cria migrações

# python manage.py migrate
# Aplica migrações no banco

# python manage.py showmigrations
# Lista as migrações


# --- ADMIN ---
# python manage.py createsuperuser
# Cria superusuário


# --- SHELL ---
# python manage.py shell
# Abre shell com Django carregado

# python manage.py shell_plus
# Shell avançado (django-extensions)


# --- BANCO DE DADOS ---
# python manage.py dbshell
# Abre o console do banco

# python manage.py inspectdb
# Gera models a partir do banco existente


# --- ARQUIVOS ESTÁTICOS ---
# python manage.py collectstatic
# Coleta arquivos estáticos (produção)


# --- TESTES ---
# python manage.py test
# Executa testes


# --- TRADUÇÃO ---
# python manage.py makemessages -l pt_BR
# Cria arquivos de tradução

# python manage.py compilemessages
# Compila traduções


# --- COMANDOS AVANÇADOS ---
# python manage.py check
# Verifica erros no projeto

# python manage.py diffsettings
# Compara configurações padrão x suas configs

# python manage.py clearsessions
# Limpa sessões expiradas

# python manage.py showurls
# Lista todas as rotas (django-extensions)


# --- DEPENDÊNCIAS ---
# pip freeze > requirements.txt
# Gera arquivo requirements

# pip install -r requirements.txt
# Instala dependências do projeto
