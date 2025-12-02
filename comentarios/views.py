from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from .models import Comentario
from .forms import ComentarioForm


@login_required
@require_http_methods(["POST"])
def criar_comentario(request, anime_id):
    """
    Criar novo comentário em um anime
    - Valida se o campo de comentário está vazio
    - Salva apenas se o usuário está logado
    - Redireciona para a página do anime
    """
    # Validar se o texto está vazio
    texto = request.POST.get('texto', '').strip()
    if not texto:
        messages.error(request, "O comentário não pode estar vazio!")
        return redirect('core:anime_detail', anime_id=anime_id)
    
    form = ComentarioForm(request.POST)
    
    if form.is_valid():
        comentario = form.save(commit=False)
        comentario.user = request.user
        comentario.anime_id = anime_id
        comentario.save()
        messages.success(request, "✓ Comentário adicionado com sucesso!")
    else:
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f"{field}: {error}")
    
    return redirect('core:anime_detail', anime_id=anime_id)


@login_required
@require_http_methods(["POST"])
def editar_comentario(request, comentario_id):
    """Editar comentário existente - apenas o dono pode editar"""
    comentario = get_object_or_404(Comentario, id=comentario_id)
    
    # Verificar se o usuário é dono do comentário
    if comentario.user != request.user:
        messages.error(request, "❌ Você não tem permissão para editar este comentário")
        return redirect('core:anime_detail', anime_id=comentario.anime_id)
    
    form = ComentarioForm(request.POST, instance=comentario)
    
    if form.is_valid():
        form.save()
        messages.success(request, "✓ Comentário atualizado com sucesso!")
    else:
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f"{field}: {error}")
    
    return redirect('core:anime_detail', anime_id=comentario.anime_id)


@login_required
@require_http_methods(["POST"])
def excluir_comentario(request, comentario_id):
    """
    Excluir comentário usando soft delete
    - Marca como deletado (is_deleted = True)
    - Não remove do banco de dados
    - Apenas o dono ou staff pode deletar
    """
    comentario = get_object_or_404(Comentario, id=comentario_id)
    
    # Verificar se o usuário é dono do comentário ou é staff
    if comentario.user != request.user and not request.user.is_staff:
        messages.error(request, "❌ Você não tem permissão para excluir este comentário")
        return redirect('core:anime_detail', anime_id=comentario.anime_id)
    
    anime_id = comentario.anime_id
    comentario.soft_delete()  # Usa soft delete
    messages.success(request, "✓ Comentário removido com sucesso!")
    
    return redirect('core:anime_detail', anime_id=anime_id)


def listar_comentarios_anime(request, anime_id):
    """
    Listar todos os comentários ATIVOS de um anime
    - Filtra apenas comentários não deletados
    - Ordena por data decrescente
    """
    comentarios = Comentario.objects.filter(
        anime_id=anime_id,
        is_deleted=False  # Mostrar apenas comentários ativos
    ).select_related('user').order_by('-criado_em')
    
    return render(request, 'comentarios/lista_comentarios.html', {
        'comentarios': comentarios,
        'anime_id': anime_id,
    })


@login_required
def meus_comentarios(request):
    """
    Listar todos os comentários do usuário logado
    - Paginação com 10 comentários por página
    - Mostra tanto ativos quanto deletados
    - Ordena por data decrescente
    """
    comentarios_do_usuario = Comentario.objects.filter(
        user=request.user
    ).select_related('user').order_by('-criado_em')
    
    # Paginação: 10 comentários por página
    paginator = Paginator(comentarios_do_usuario, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'comentarios/meus_comentarios.html', {
        'page_obj': page_obj,
        'comentarios': page_obj.object_list,
        'total': paginator.count,
    })

