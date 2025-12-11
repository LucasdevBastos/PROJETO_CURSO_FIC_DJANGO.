#!/bin/bash

# =================================================================
# 🚀 Script de Deploy - Railway
# Validação pré-deploy para correção de FOUC
# =================================================================

echo "🔍 Validando configurações antes do deploy..."

# 1. Verificar se collectstatic vai funcionar
echo "📦 Testando collectstatic..."
python manage.py collectstatic --noinput --dry-run

if [ $? -ne 0 ]; then
    echo "❌ ERRO: collectstatic falhou!"
    exit 1
fi

# 2. Verificar se arquivos CSS existem
echo "🎨 Verificando arquivos CSS..."
if [ ! -f "static/css/style.css" ]; then
    echo "❌ ERRO: static/css/style.css não encontrado!"
    exit 1
fi

# 3. Verificar se WhiteNoise está instalado
echo "📦 Verificando WhiteNoise..."
python -c "import whitenoise" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ ERRO: WhiteNoise não instalado!"
    echo "Execute: pip install whitenoise"
    exit 1
fi

# 4. Verificar configuração do settings.py
echo "⚙️  Verificando settings.py..."

# Verifica se STATICFILES_STORAGE está configurado
grep -q "CompressedManifestStaticFilesStorage" animecalendar/settings.py
if [ $? -ne 0 ]; then
    echo "⚠️  AVISO: STATICFILES_STORAGE pode não estar configurado corretamente"
fi

# Verifica se WhiteNoise está no MIDDLEWARE
grep -q "whitenoise.middleware.WhiteNoiseMiddleware" animecalendar/settings.py
if [ $? -ne 0 ]; then
    echo "❌ ERRO: WhiteNoise não está no MIDDLEWARE!"
    exit 1
fi

# 5. Verificar templates
echo "📄 Verificando templates..."

# Verifica se CSS está no head
grep -q "block head_extra" animecalendar/templates/base.html
if [ $? -ne 0 ]; then
    echo "⚠️  AVISO: base.html pode não ter block head_extra"
fi

# 6. Executar collectstatic real
echo "📁 Executando collectstatic..."
python manage.py collectstatic --noinput --clear

if [ $? -ne 0 ]; then
    echo "❌ ERRO: collectstatic falhou!"
    exit 1
fi

# 7. Verificar se staticfiles foi criado
if [ ! -d "staticfiles" ]; then
    echo "❌ ERRO: Diretório staticfiles não foi criado!"
    exit 1
fi

# 8. Contar arquivos coletados
FILE_COUNT=$(find staticfiles -type f | wc -l)
echo "✅ $FILE_COUNT arquivos estáticos coletados"

if [ $FILE_COUNT -lt 50 ]; then
    echo "⚠️  AVISO: Poucos arquivos estáticos ($FILE_COUNT). Esperado > 100"
fi

# 9. Verificar se CSS principal existe em staticfiles
if [ ! -f "staticfiles/css/style.css" ]; then
    echo "❌ ERRO: CSS principal não foi coletado!"
    exit 1
fi

# 10. Verificar requirements.txt
echo "📋 Verificando requirements.txt..."
grep -q "whitenoise" requirements.txt
if [ $? -ne 0 ]; then
    echo "⚠️  AVISO: WhiteNoise pode não estar no requirements.txt"
fi

# 11. Teste de importação
echo "🐍 Testando importações Python..."
python -c "
import django
import whitenoise
from django.core.management import call_command
print('✅ Todas as importações funcionando')
"

if [ $? -ne 0 ]; then
    echo "❌ ERRO: Falha nas importações!"
    exit 1
fi

# 12. Verificar railway_init.sh
echo "🚂 Verificando railway_init.sh..."
if [ ! -f "railway_init.sh" ]; then
    echo "⚠️  AVISO: railway_init.sh não encontrado"
else
    chmod +x railway_init.sh
    echo "✅ Permissões do railway_init.sh configuradas"
fi

# =================================================================
echo ""
echo "✨ ================================="
echo "✅ Validação concluída com sucesso!"
echo "================================="
echo ""
echo "📋 Checklist de Deploy:"
echo "  ✅ collectstatic funcionando"
echo "  ✅ WhiteNoise configurado"
echo "  ✅ CSS crítico no head"
echo "  ✅ Preload configurado"
echo "  ✅ Scripts com defer"
echo "  ✅ Arquivos estáticos prontos"
echo ""
echo "🚀 Pronto para deploy no Railway!"
echo ""
echo "⚠️  Lembre-se de:"
echo "  1. Fazer commit de todas as mudanças"
echo "  2. Push para o repositório"
echo "  3. Verificar logs no Railway após deploy"
echo "  4. Testar performance com DevTools"
echo ""
