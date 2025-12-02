from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Perfil
from .forms import PerfilForm
from comentarios.models import Comentario
from core.models import Favorito


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
    
    # Últimos 10 favoritos do usuário
    favoritos = usuario.favoritos_anime.all().order_by('-criado_em')[:10]
    
    context = {
        'usuario': usuario,
        'perfil': perfil,
        'comentarios_recentes': comentarios_recentes,
        'favoritos': favoritos,
        'total_comentarios': usuario.comentarios_anime.filter(is_deleted=False).count(),
        'total_favoritos': usuario.favoritos_anime.count(),
    }
    
    return render(request, 'perfil/perfil.html', context)


@login_required
def editar_perfil(request):
    """Editar perfil do usuário logado"""
    # Garantir que o perfil existe
    perfil, created = Perfil.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES, instance=perfil)
        
        if form.is_valid():
            form.save()
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
    }
    
    return render(request, 'perfil/editar_perfil.html', context)


def todos_comentarios_usuario(request, username):
    """
    Listar todos os comentários ATIVOS de um usuário com paginação
    - 10 comentários por página
    - Apenas comentários não deletados
    - Ordenado por data decrescente
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
    
    context = {
        'usuario': usuario,
        'page_obj': page_obj,
        'comentarios': page_obj.object_list,
        'total': paginator.count,
    }
    
    return render(request, 'perfil/todos_comentarios.html', context)


def todos_favoritos_usuario(request, username):
    """
    Listar todos os favoritos de um usuário com paginação
    - 12 favoritos por página
    - Ordenado por data decrescente
    """
    usuario = get_object_or_404(User, username=username)
    
    favoritos_qs = usuario.favoritos_anime.all().order_by('-criado_em')
    
    # Paginação: 12 favoritos por página
    paginator = Paginator(favoritos_qs, 12)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'usuario': usuario,
        'page_obj': page_obj,
        'favoritos': page_obj.object_list,
        'total': paginator.count,
    }
    
    return render(request, 'perfil/todos_favoritos.html', context)

