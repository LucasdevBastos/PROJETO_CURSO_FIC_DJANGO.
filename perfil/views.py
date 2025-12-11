from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Perfil
from .forms import PerfilForm
from comentarios.models import Comentario
from core.models import Favorito
from core.jikan_api import JikanAPI


def perfil_usuario(request, username):
    """
    Exibir perfil de um usuário
    - Mostra últimos comentários ATIVOS
    - Mostra últimos favoritos
    - Cria perfil se não existir
    """
    usuario = get_object_or_404(User, username=username)
    
    # Verificar se o usuário tem perfil, se não criar um
    try:
        perfil = usuario.perfil
    except Perfil.DoesNotExist:
        perfil = Perfil.objects.create(user=usuario)
        messages.info(request, f"Perfil criado para {username}")
    
    # Últimos 5 comentários ATIVOS do usuário
    comentarios_recentes = usuario.comentarios_anime.filter(
        is_deleted=False  # Apenas ativos
    ).order_by('-criado_em')[:5]
    
    # Enriquecer comentários com dados da API
    comentarios_enriquecidos = []
    for coment in comentarios_recentes:
        anime = JikanAPI.get_anime_by_id(coment.anime_id)
        if anime:
            comentarios_enriquecidos.append({
                'comentario': coment,
                'anime': anime,
            })
    
    # Últimos 10 favoritos do usuário
    favoritos = usuario.favoritos_anime.all().order_by('-criado_em')[:10]
    
    # Enriquecer favoritos com dados da API
    favoritos_enriquecidos = []
    for fav in favoritos:
        anime = JikanAPI.get_anime_by_id(fav.anime_id)
        if anime:
            favoritos_enriquecidos.append({
                'favorito': fav,
                'anime': anime,
            })
    
    context = {
        'usuario': usuario,
        'perfil': perfil,
        'comentarios_recentes': comentarios_recentes,
        'comentarios_enriquecidos': comentarios_enriquecidos,
        'favoritos': favoritos,
        'favoritos_enriquecidos': favoritos_enriquecidos,
        'total_comentarios': usuario.comentarios_anime.filter(is_deleted=False).count(),
        'total_favoritos': usuario.favoritos_anime.count(),
    }
    
    return render(request, 'perfil/perfil.html', context)


@login_required
def editar_perfil(request):
    """
    Editar perfil do usuário logado
    
    Regras:
    - Todos podem editar avatar_choice (avatares padrão) e bio
    - Apenas VIP pode editar custom_avatar e custom_banner
    """
    # Garantir que o perfil existe
    perfil, created = Perfil.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES, instance=perfil)
        
        if form.is_valid():
            # Salvar o formulário
            perfil_atualizado = form.save(commit=False)
            
            # Garantir que não-VIP não possam ter campos personalizados
            # (redundância de segurança, já está no model.save() e form.clean())
            if not perfil_atualizado.is_vip:
                perfil_atualizado.custom_avatar = None
                perfil_atualizado.custom_banner = None
            
            perfil_atualizado.save()
            
            # Mensagem baseada em status VIP
            if perfil.is_vip:
                messages.success(request, "Perfil VIP atualizado com sucesso!")
            else:
                messages.success(request, "Perfil atualizado com sucesso!")
            
            return redirect('perfil:ver', username=request.user.username)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = PerfilForm(instance=perfil)
    
    context = {
        'form': form,
        'perfil': perfil,
        'is_vip': perfil.is_vip,  # Para uso no template
        'avatar_choices': Perfil.AVATAR_CHOICES,  # Para preview dos avatares
    }
    
    return render(request, 'perfil/editar_perfil.html', context)


def todos_comentarios_usuario(request, username):
    """
    Listar todos os comentários ATIVOS de um usuário com paginação
    - 10 comentários por página
    - Apenas comentários não deletados
    - Ordenado por data decrescente
    - Enriquecido com dados da API
    """
    usuario = get_object_or_404(User, username=username)
    
    # Filtrar apenas comentários ativos
    comentarios_qs = usuario.comentarios_anime.filter(
        is_deleted=False
    ).order_by('-criado_em')
    
    # Paginação: 10 comentários por página
    paginator = Paginator(comentarios_qs, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    # Enriquecer com dados da API
    comentarios_enriquecidos = []
    for coment in page_obj.object_list:
        anime = JikanAPI.get_anime_by_id(coment.anime_id)
        if anime:
            comentarios_enriquecidos.append({
                'comentario': coment,
                'anime': anime,
            })
    
    context = {
        'usuario': usuario,
        'page_obj': page_obj,
        'comentarios': page_obj.object_list,
        'comentarios_enriquecidos': comentarios_enriquecidos,
        'total': paginator.count,
    }
    
    return render(request, 'perfil/todos_comentarios.html', context)


def todos_favoritos_usuario(request, username):
    """
    Listar todos os favoritos de um usuário com paginação
    - 12 favoritos por página
    - Ordenado por data decrescente
    - Enriquecido com dados da API
    """
    usuario = get_object_or_404(User, username=username)
    
    favoritos_qs = usuario.favoritos_anime.all().order_by('-criado_em')
    
    # Paginação: 12 favoritos por página
    paginator = Paginator(favoritos_qs, 12)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    # Enriquecer com dados da API
    animes_favoritos = []
    for fav in page_obj.object_list:
        anime = JikanAPI.get_anime_by_id(fav.anime_id)
        if anime:
            animes_favoritos.append({
                'favorito': fav,
                'anime': anime,
            })
    
    context = {
        'usuario': usuario,
        'page_obj': page_obj,
        'favoritos': page_obj.object_list,
        'animes_favoritos': animes_favoritos,
        'total': paginator.count,
    }
    
    return render(request, 'perfil/todos_favoritos.html', context)

