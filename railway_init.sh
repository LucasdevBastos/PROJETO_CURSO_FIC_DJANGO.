#!/bin/bash

echo "🚀 Inicializando aplicação Django no Railway..."

# 1. Aplicar migrações
echo "📦 Aplicando migrações do banco de dados..."
python manage.py migrate --noinput

# 2. Coletar arquivos estáticos
echo "📁 Coletando arquivos estáticos..."
python manage.py collectstatic --noinput --clear

# 3. Criar superuser se não existir
echo "👤 Verificando superuser..."
python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123');
    print('✅ Superuser criado: admin / admin123');
else:
    print('ℹ️  Superuser já existe');
" || echo "⚠️  Erro ao criar superuser (pode ser normal se já existir)"

# 4. Importar animes da API
echo "🎬 Importando animes da Jikan API..."
python manage.py import_animes --limit 100 || echo "⚠️  Erro ao importar animes (verifique os logs)"

echo "✅ Inicialização concluída!"
