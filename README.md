# 🎌 Anime Calendar – Calendário de Animes

Um sistema em **Django** para organizar e visualizar animes por temporada, integrando dados do **MyAnimeList** (via **Jikan API**) e permitindo visualizar animes em **cards bonitos com Bootstrap**.

A ideia é ser um **hub visual** onde o usuário consiga:

- Ver os animes cadastrados no banco (projeto próprio).
- Ver animes da **temporada atual** diretamente do MyAnimeList.
- Evoluir para um calendário completo de lançamentos de episódios, comentários e mais.

---

## 🧩 Tecnologias utilizadas

- **Python 3.13+**
- **Django 5.2**
- **SQLite** (banco padrão para desenvolvimento)
- **Bootstrap 5** (via CDN)
- **Jikan API** – wrapper público para o MyAnimeList  
  👉 https://docs.api.jikan.moe/

Apps principais do projeto:

- `anime` – modelos de animes, temporadas etc.
- `calendar_app` – (futuro) visualização em calendário.
- `comments` – comentários dos usuários sobre animes.
- `users` – gerenciamento de usuários (auth).
- `core` – utilidades / lógica compartilhada.

---

## 📁 Estrutura básica do projeto

```text
projeto_curso_fic_django/
├─ manage.py
├─ db.sqlite3
├─ animecalendar/
│  ├─ settings.py
│  ├─ urls.py
│  ├─ wsgi.py
│  └─ asgi.py
├─ anime/
│  ├─ models.py
│  ├─ views.py
│  ├─ urls.py
│  └─ templates/
│     └─ anime_list.html
├─ comments/
│  └─ ...
├─ calendar_app/
│  └─ ...
├─ core/
│  └─ ...
├─ users/
│  └─ ...
└─ templates/
   └─ base.html
