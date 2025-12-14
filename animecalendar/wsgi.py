"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "animecalendar.settings")


application = get_wsgi_application()

# Criar superuser automaticamente no Railway
def create_initial_superuser():
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        username = 'admin_railway'
        email = 'admin@animecalendar.com'
        password = 'Railway2025@Admin'
        
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            print(f'✅ Superuser "{username}" criado com sucesso!')
            print(f'Username: {username}')
            print(f'Email: {email}')
            print(f'Password: {password}')
    except Exception as e:
        print(f'⚠️ Erro ao criar superuser: {e}')

# Executa a criação do superuser apenas uma vez
create_initial_superuser()

