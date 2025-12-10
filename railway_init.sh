#!/bin/bash

echo "🚀 Inicializando aplicação Django no Railway..."

# 1. Aplicar migrações
echo "📦 Aplicando migrações do banco de dados..."
python manage.py migrate --noinput

# 2. Criar superuser se não existir
echo "👤 Verificando superuser..."
python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123');
    print('✅ Superuser criado: admin / admin123');
else:
    print('ℹ️  Superuser já existe');
"

# 3. Importar animes da API
echo "🎬 Importando animes da Jikan API..."
python manage.py import_animes --limit 100

# 4. Coletar arquivos estáticos
echo "📁 Coletando arquivos estáticos..."
python manage.py collectstatic --noinput --clear

echo "✅ Inicialização concluída!"
