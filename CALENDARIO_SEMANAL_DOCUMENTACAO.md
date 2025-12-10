# 📅 Sistema de Calendário Semanal de Animes - Documentação

## ✅ Implementado em 8 de dezembro de 2025

Implementei um **calendário semanal de animes** que mostra os lançamentos organizados por dia da semana, usando a **Jikan API** (wrapper oficial do MyAnimeList).

---

## 🎯 O Problema que Foi Resolvido

**ANTES:**
- O calendário mostrava **todos os animes em todos os dias** (repetição)
- Não havia separação por dia da semana
- Dados desatualizados do banco de dados local

**DEPOIS:**
- Cada anime aparece **apenas no dia correto** de exibição
- Dados **atualizados em tempo real** da Jikan API
- Cache de 4 horas para performance
- Calendário organizado por dias da semana (Segunda a Domingo)

---

## 📁 Arquivos Criados/Modificados

### 1. **Novo Template - Calendário Semanal**
📄 `calendar_app/templates/calendar_app/calendario.html`

**Funcionalidades:**
- ✅ Grid responsivo com 7 cards (um para cada dia da semana)
- ✅ Cada dia mostra apenas os animes que lançam naquele dia
- ✅ Cards com poster, título, horário, score e tipo
- ✅ Link direto para MyAnimeList
- ✅ Empty state quando não há animes no dia
- ✅ Contador de animes por dia
- ✅ Design glass morphism consistente com o resto do site

**Estrutura do Template:**
```django
{% for anime in calendario.monday %}
    <!-- Anime só aparece na segunda -->
{% endfor %}

{% for anime in calendario.tuesday %}
    <!-- Anime só aparece na terça -->
{% endfor %}
...
```

---

### 2. **Nova View - Calendário Semanal**
📄 `calendar_app/views.py`

**Função Adicionada:**
```python
@login_required
def calendario_semanal(request):
    """
    Mostra o calendário semanal com animes organizados por dia da semana.
    Usa a Jikan API para buscar os animes de cada dia.
    """
```

**Como Funciona:**
1. Cria um dicionário com 7 chaves (monday, tuesday, ..., sunday)
2. Para cada dia, chama `AnimeScheduleService.get_animes_by_weekday()`
3. Faz parse dos dados com `parse_anime_data()`
4. Retorna o dicionário para o template

**Estrutura de Dados Retornada:**
```python
{
    "monday": [
        {
            "mal_id": 12345,
            "title": "One Piece",
            "image_url": "https://...",
            "score": 8.5,
            "broadcast_time": "23:30",
            "type": "TV",
            "episodes": 24,
            "url": "https://myanimelist.net/...",
            ...
        },
        ...
    ],
    "tuesday": [...],
    ...
}
```

---

### 3. **Serviço de API (Já Existia)**
📄 `calendar_app/services.py`

**Classes Principais:**
- `AnimeScheduleService` - Integração com Jikan API
- `CacheService` - Gerenciamento de cache

**Métodos Importantes:**

#### `get_animes_by_weekday(weekday_name: str)`
Busca animes de um dia específico da semana.

**Parâmetros:**
- `weekday_name`: "monday", "tuesday", "wednesday", etc.

**Retorna:**
- Lista de dicts com dados brutos da API

**Cache:**
- Chave: `jikan_schedule_{weekday_name}`
- Duração: 4 horas
- Se cache existir, não faz chamada à API

**Exemplo de Uso:**
```python
animes = AnimeScheduleService.get_animes_by_weekday("monday")
# Retorna todos os animes de segunda-feira
```

#### `parse_anime_data(anime: dict)`
Extrai e formata dados importantes do anime.

**Campos Extraídos:**
- `title` - Título principal
- `title_english` - Título em inglês
- `image_url` - URL da capa (prioriza large)
- `score` - Nota do MAL (0-10)
- `broadcast_time` - Horário de exibição (ex: "23:30")
- `episodes` - Número de episódios
- `type` - Tipo (TV, OVA, Movie, etc.)
- `status` - Status (Airing, Finished, etc.)
- `url` - Link para MyAnimeList

**Exemplo:**
```python
anime_raw = {...}  # Dados da API
anime_parsed = AnimeScheduleService.parse_anime_data(anime_raw)
# Retorna dict limpo e formatado
```

---

### 4. **URLs Atualizadas**
📄 `calendar_app/urls.py`

**Antes:**
```python
urlpatterns = [
    path("", views.month_current, name="month_current"),
    path("<int:year>/<int:month>/", views.month_view, name="month_view"),
]
```

**Depois:**
```python
urlpatterns = [
    # Calendário semanal (padrão) - /calendario/
    path("", views.calendario_semanal, name="calendario_semanal"),
    
    # Calendário mensal - /calendario/mes/
    path("mes/", views.month_current, name="month_current"),
    path("mes/<int:year>/<int:month>/", views.month_view, name="month_view"),
]
```

**Mudanças:**
- ✅ `/calendario/` agora mostra o **calendário semanal** (novo)
- ✅ `/calendario/mes/` mostra o calendário mensal (antigo)
- ✅ Ambos convivem no sistema

---

## 🔄 Como o Sistema Funciona

### Fluxo Completo:

```
1. Usuário acessa /calendario/
           ↓
2. View calendario_semanal() é chamada
           ↓
3. Para cada dia da semana:
   ├─ Verifica se existe cache (jikan_schedule_monday)
   │  ├─ SIM: Retorna dados do cache
   │  └─ NÃO: ↓
   ├─ Faz chamada HTTP para Jikan API
   │  URL: https://api.jikan.moe/v4/schedules?filter=monday&limit=25
   ├─ Recebe JSON com lista de animes
   ├─ Salva no cache por 4 horas
   └─ Faz parse dos dados
           ↓
4. Monta dicionário com 7 listas (uma por dia)
           ↓
5. Envia para template calendario.html
           ↓
6. Template renderiza 7 cards (Segunda a Domingo)
   Cada card mostra apenas os animes daquele dia
           ↓
7. Usuário vê calendário atualizado
```

---

## 🌐 Integração com Jikan API

### Endpoint Usado:
```
GET https://api.jikan.moe/v4/schedules
```

**Parâmetros:**
- `filter`: Dia da semana (monday, tuesday, etc.)
- `limit`: Número máximo de animes (25)
- `page`: Página de resultados (1)

**Exemplo de Requisição:**
```python
response = requests.get(
    "https://api.jikan.moe/v4/schedules",
    params={
        "filter": "monday",
        "limit": 25,
        "page": 1,
    },
    timeout=5,
)
```

**Resposta (JSON):**
```json
{
  "data": [
    {
      "mal_id": 51535,
      "title": "One Piece",
      "images": {
        "jpg": {
          "image_url": "https://...",
          "large_image_url": "https://..."
        }
      },
      "score": 8.5,
      "broadcast": {
        "string": "Sundays at 23:30 (JST)"
      },
      "type": "TV",
      "episodes": 1000,
      ...
    },
    ...
  ]
}
```

---

## 💾 Sistema de Cache

### Por que Cache?

1. **Performance:** API externa pode ser lenta
2. **Rate Limiting:** Jikan API tem limite de requisições
3. **Disponibilidade:** Se API cair, ainda temos dados
4. **Economia de Banda:** Menos requisições HTTP

### Implementação:

**Chaves de Cache:**
```python
jikan_schedule_monday
jikan_schedule_tuesday
jikan_schedule_wednesday
jikan_schedule_thursday
jikan_schedule_friday
jikan_schedule_saturday
jikan_schedule_sunday
```

**Duração:** 4 horas (14400 segundos)

**Backend:** Django Cache Framework (configurado em settings.py)

### Como Limpar o Cache:

**Via Python Shell:**
```python
from calendar_app.services import CacheService
CacheService.clear_schedule_cache()
```

**Via Terminal:**
```bash
python manage.py shell
>>> from django.core.cache import cache
>>> cache.delete('jikan_schedule_monday')
```

---

## 🎨 Design e Layout

### Estrutura Visual:

```
┌─────────────────────────────────────┐
│      CALENDÁRIO SEMANAL DE ANIMES    │
│   Veja quais animes lançam em cada   │
│            dia da semana             │
└─────────────────────────────────────┘

┌──────────┬──────────┬──────────┐
│ Segunda  │  Terça   │  Quarta  │
│ 5 animes │ 8 animes │ 3 animes │
├──────────┼──────────┼──────────┤
│  Quinta  │  Sexta   │  Sábado  │
│ 12 animes│ 6 animes │ 10 animes│
├──────────┴──────────┴──────────┤
│           Domingo              │
│          15 animes             │
└────────────────────────────────┘
```

### Cada Card de Dia Contém:

- **Header:** Nome do dia + contador de animes
- **Lista de Animes:** Scrollável (max 600px)
  - Poster (80x110px)
  - Título
  - Horário de exibição
  - Score (nota do MAL)
  - Tipo (TV, OVA, etc.)
  - Número de episódios
  - Botão "Ver no MAL"

### Responsividade:

- **Desktop (≥768px):** Grid de 3-4 colunas
- **Tablet (≤768px):** 1 coluna, posters maiores
- **Mobile (≤480px):** Layout compacto

---

## 📝 Campos Disponíveis de Cada Anime

### No Template:
```django
{{ anime.title }}              {# Título principal #}
{{ anime.title_english }}      {# Título em inglês #}
{{ anime.image_url }}          {# URL da capa #}
{{ anime.score }}              {# Nota (8.5) #}
{{ anime.broadcast_time }}     {# Horário (23:30) #}
{{ anime.broadcast_string }}   {# "Sundays at 23:30" #}
{{ anime.type }}               {# TV, OVA, Movie, etc. #}
{{ anime.episodes }}           {# Número de episódios #}
{{ anime.status }}             {# Airing, Finished, etc. #}
{{ anime.url }}                {# Link para MAL #}
{{ anime.mal_id }}             {# ID do MyAnimeList #}
{{ anime.synopsis }}           {# Sinopse (200 chars) #}
{{ anime.source }}             {# Manga, Light Novel, etc. #}
{{ anime.rank }}               {# Ranking no MAL #}
```

---

## 🔧 Como Personalizar

### 1. Trocar a API

Se quiser usar outra API (AniList, Kitsu, etc.), edite:

📄 `calendar_app/services.py`

```python
# Linha 21 - URL da API
JIKAN_SCHEDULE_URL = "https://api.jikan.moe/v4/schedules"

# Mudar para:
JIKAN_SCHEDULE_URL = "https://api.outra-api.com/schedule"
```

**Também ajuste:**
- Parâmetros da requisição (linha 54-58)
- Parse dos dados (linha 107-148)

---

### 2. Alterar Limite de Animes por Dia

📄 `calendar_app/services.py` (linha 57)

```python
params={
    "filter": weekday_name,
    "limit": 25,  # MUDAR AQUI (máximo: 25)
    "page": 1,
},
```

**Valores possíveis:** 1-25 por página

---

### 3. Mudar Duração do Cache

📄 `calendar_app/services.py` (linha 24)

```python
CACHE_DURATION = 3600 * 4  # 4 horas (14400 segundos)

# Exemplos:
CACHE_DURATION = 3600        # 1 hora
CACHE_DURATION = 3600 * 12   # 12 horas
CACHE_DURATION = 86400       # 1 dia
```

---

### 4. Adicionar Filtros

No template, você pode filtrar animes por score, tipo, etc.:

```django
{% for anime in calendario.monday %}
    {% if anime.score >= 8.0 %}
        <!-- Só mostra animes com nota >= 8 -->
    {% endif %}
{% endfor %}
```

---

### 5. Ordenar Animes

Na view, após buscar os dados:

```python
# Ordenar por score (maior primeiro)
calendario[weekday_name] = sorted(
    calendario[weekday_name],
    key=lambda x: x.get("score", 0),
    reverse=True
)

# Ou por horário
calendario[weekday_name] = sorted(
    calendario[weekday_name],
    key=lambda x: x.get("broadcast_time", "")
)
```

---

## 🧪 Como Testar

### 1. Teste Básico
```bash
1. Acesse http://127.0.0.1:8000/calendario/
2. Veja os 7 cards (Segunda a Domingo)
3. Cada card deve mostrar animes diferentes
4. Verifique que não há repetição
```

### 2. Teste de Cache
```bash
1. Acesse /calendario/ (primeira vez - faz requisição à API)
2. Recarregue a página (segunda vez - usa cache)
3. Verifique no terminal os logs:
   [CACHE HIT] Agenda para monday
   [CACHE HIT] Agenda para tuesday
   ...
```

### 3. Teste de Empty State
```bash
1. Se algum dia não tiver animes, deve aparecer:
   "Nenhum anime confirmado para [dia]."
```

### 4. Teste de API Offline
```bash
1. Desconecte a internet
2. Acesse /calendario/
3. Se tiver cache: mostra dados antigos
4. Se não tiver cache: mostra empty state
```

---

## 🐛 Troubleshooting

### Problema: "Nenhum anime confirmado" em todos os dias

**Causas:**
1. API offline
2. Rate limiting
3. Timeout
4. Erro de conexão

**Solução:**
```bash
# Ver logs no terminal
python manage.py runserver

# Limpar cache e tentar novamente
python manage.py shell
>>> from calendar_app.services import CacheService
>>> CacheService.clear_schedule_cache()
```

---

### Problema: Animes aparecem em dias errados

**Causa:** API pode estar retornando dados incorretos

**Solução:**
1. Verificar resposta da API manualmente
2. Ajustar lógica de parse se necessário

```python
# Em services.py, adicionar logs
logger.info(f"[DEBUG] Broadcast: {anime.get('broadcast')}")
```

---

### Problema: Página carrega lenta

**Causa:** Fazendo 7 requisições à API sem cache

**Solução:**
- Cache já está implementado
- Aguardar 1-2 segundos na primeira carga
- Carregamentos seguintes serão instantâneos (cache)

---

### Problema: Imagens não carregam

**Causa:** URLs da API podem estar quebradas

**Solução:**
```python
# Em services.py (linha 119-123)
# Já tem fallback para diferentes resoluções
image_url = (
    images.get("jpg", {}).get("large_image_url") or
    images.get("jpg", {}).get("image_url") or
    ""  # Fallback vazio
)
```

---

## 📊 Estatísticas da Implementação

| Métrica | Valor |
|---------|-------|
| Arquivos criados | 2 |
| Arquivos modificados | 2 |
| Linhas de código (template) | ~600 |
| Linhas de código (view) | ~40 |
| API endpoints usados | 1 |
| Tempo de cache | 4 horas |
| Animes por dia (max) | 25 |
| Dias da semana | 7 |
| Requisições por carga | 0-7 (depende do cache) |

---

## 🚀 Melhorias Futuras (Opcional)

### 1. Filtro por Temporada
Adicionar filtro para ver só animes da temporada atual (Winter, Spring, Summer, Fall).

### 2. Busca por Gênero
Permitir filtrar animes por gênero (Action, Romance, etc.).

### 3. Sistema de Notificações
Notificar usuário quando anime favorito lançar episódio novo.

### 4. Integração com Banco Local
Cruzar dados da API com animes do banco local para adicionar informações extras.

### 5. Modo Escuro/Claro
Toggle para alternar tema.

### 6. Exportar Calendário
Botão para exportar como iCal/Google Calendar.

---

## 🎉 Conclusão

O calendário agora está **100% funcional** e mostra os animes corretos de cada dia da semana, sem repetições.

### Benefícios:

✅ **Dados atualizados** - API do MyAnimeList via Jikan  
✅ **Performance** - Cache de 4 horas  
✅ **Organização** - Cada anime no dia correto  
✅ **Design moderno** - Glass morphism consistente  
✅ **Responsivo** - Funciona em desktop, tablet e mobile  
✅ **Escalável** - Fácil trocar de API ou adicionar features  

---

## 📚 Referências

- **Jikan API Docs:** https://docs.api.jikan.moe/
- **MyAnimeList:** https://myanimelist.net/
- **Django Cache:** https://docs.djangoproject.com/en/stable/topics/cache/

---

**Data:** 8 de dezembro de 2025  
**Status:** ✅ Implementado e Testado  
**URL:** http://127.0.0.1:8000/calendario/  
**API:** Jikan v4 (MyAnimeList)
