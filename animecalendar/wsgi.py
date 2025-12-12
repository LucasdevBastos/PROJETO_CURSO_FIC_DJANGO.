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

from django.contrib.auth import get_user_model
User = get_user_model()
u = User.objects.get(username="LucasADM")
u.set_password("@Lucas9800")
u.save()
print("Senha do usuário 'LucasADM' atualizada com sucesso.")
