from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Comentario
from .forms import ComentarioForm


@login_required
@require_http_methods(["POST"])
def criar_comentario(request, anime_id):
    """Criar novo comentário em um anime"""
    form = ComentarioForm(request.POST)
    
    if form.is_valid():
        comentario = form.save(commit=False)
        comentario.user = request.user
        comentario.anime_id = anime_id
        comentario.save()
        messages.success(request, "Comentário adicionado com sucesso!")
    else:
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f"{field}: {error}")
    
    # Redireciona para a página do anime
    return redirect('anime_detail', anime_id=anime_id)


@login_required
@require_http_methods(["POST"])
def editar_comentario(request, comentario_id):
    """Editar comentário existente"""
    comentario = get_object_or_404(Comentario, id=comentario_id)
    
    # Verificar se o usuário é dono do comentário
    if comentario.user != request.user:
        messages.error(request, "Você não tem permissão para editar este comentário")
        return redirect('anime_detail', anime_id=comentario.anime_id)
    
    form = ComentarioForm(request.POST, instance=comentario)
    
    if form.is_valid():
        form.save()
        messages.success(request, "Comentário atualizado com sucesso!")
    else:
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f"{field}: {error}")
    
    return redirect('anime_detail', anime_id=comentario.anime_id)


@login_required
@require_http_methods(["POST"])
def excluir_comentario(request, comentario_id):
    """Excluir comentário"""
    comentario = get_object_or_404(Comentario, id=comentario_id)
    
    # Verificar se o usuário é dono do comentário
    if comentario.user != request.user and not request.user.is_staff:
        messages.error(request, "Você não tem permissão para excluir este comentário")
        return redirect('anime_detail', anime_id=comentario.anime_id)
    
    anime_id = comentario.anime_id
    comentario.delete()
    messages.success(request, "Comentário excluído com sucesso!")
    
    return redirect('anime_detail', anime_id=anime_id)


def listar_comentarios_anime(request, anime_id):
    """Listar todos os comentários de um anime"""
    comentarios = Comentario.objects.filter(anime_id=anime_id).select_related('user')
    
    return render(request, 'comentarios/lista_comentarios.html', {
        'comentarios': comentarios,
        'anime_id': anime_id,
    })
