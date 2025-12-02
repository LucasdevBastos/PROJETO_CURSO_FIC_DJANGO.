from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Favorito
from .jikan_api import JikanAPI
from comentarios.models import Comentario
from comentarios.forms import ComentarioForm
import logging

logger = logging.getLogger(__name__)


def anime_detail(request, anime_id):
    """
    Exibir página detalhada de um anime
    """
    # Buscar dados do anime na Jikan API
    anime = JikanAPI.get_anime_by_id(anime_id)
    
    if not anime:
        messages.error(request, "Anime não encontrado")
        return redirect('landing')
    
    # Buscar comentários do anime
    comentarios = Comentario.objects.filter(anime_id=anime_id).select_related('user')
    
    # Verificar se o usuário já favoritou este anime
    ja_favoritado = False
    if request.user.is_authenticated:
        ja_favoritado = Favorito.objects.filter(
            user=request.user,
            anime_id=anime_id
        ).exists()
    
    # Form para novo comentário
    form_comentario = None
    if request.user.is_authenticated:
        form_comentario = ComentarioForm()
    
    context = {
        'anime': anime,
        'anime_id': anime_id,
        'comentarios': comentarios,
        'ja_favoritado': ja_favoritado,
        'form_comentario': form_comentario,
    }
    
    return render(request, 'core/anime_detail.html', context)


@login_required
@require_http_methods(["POST"])
def toggle_favorito(request, anime_id):
    """
    Toggle para adicionar/remover favorito
    """
    # Verificar se o anime existe na API antes de favoritá-lo
    anime = JikanAPI.get_anime_by_id(anime_id)
    if not anime:
        messages.error(request, "Anime não encontrado")
        return redirect('landing')
    
    # Toggle favorito
    favorito, criado = Favorito.objects.get_or_create(
        user=request.user,
        anime_id=anime_id
    )
    
    if not criado:
        # Já existia, então removemos
        favorito.delete()
        messages.success(request, "Removido dos favoritos!")
        acao = 'removido'
    else:
        # Acabou de ser criado
        messages.success(request, "Adicionado aos favoritos!")
        acao = 'adicionado'
    
    # Se for requisição AJAX, retorna JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'acao': acao,
            'ja_favoritado': criado,
        })
    
    # Caso contrário, redireciona para a página do anime
    return redirect('core:anime_detail', anime_id=anime_id)


def listar_favoritos(request):
    """
    Listar os favoritos do usuário logado
    """
    if not request.user.is_authenticated:
        messages.warning(request, "Você precisa estar logado para ver seus favoritos")
        return redirect('users:login')
    
    favoritos = request.user.favoritos_anime.all()
    
    # Enriquecer com dados da API
    animes_favoritos = []
    for fav in favoritos:
        anime = JikanAPI.get_anime_by_id(fav.anime_id)
        if anime:
            animes_favoritos.append({
                'favorito': fav,
                'anime': anime,
            })
    
    context = {
        'favoritos': favoritos,
        'animes_favoritos': animes_favoritos,
        'total': len(animes_favoritos),
    }
    
    return render(request, 'core/favoritos.html', context)
