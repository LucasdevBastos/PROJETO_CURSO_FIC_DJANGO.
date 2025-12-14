import os
import django

# Configurar o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'animecalendar.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Credenciais do superuser
username = 'admin_railway'
email = 'admin@animecalendar.com'
password = 'Railway2025@Admin'

# Verificar se o usuário já existe
if User.objects.filter(username=username).exists():
    print(f'❌ Usuário "{username}" já existe!')
    user = User.objects.get(username=username)
    # Atualizar a senha
    user.set_password(password)
    user.save()
    print(f'✅ Senha do usuário "{username}" foi atualizada!')
else:
    # Criar o superuser
    user = User.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )
    print(f'✅ Superuser "{username}" criado com sucesso!')

print('\n' + '='*50)
print('CREDENCIAIS DO SUPERUSER PARA RAILWAY:')
print('='*50)
print(f'Username: {username}')
print(f'Email: {email}')
print(f'Password: {password}')
print('='*50)
print('\nGuarde essas credenciais em um local seguro!')
