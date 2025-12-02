from django.urls import path
from . import views

app_name = 'comentarios'

urlpatterns = [
    # Criar comentário em um anime
    path('anime/<int:anime_id>/criar/', views.criar_comentario, name='criar'),
    
    # Editar comentário existente
    path('<int:comentario_id>/editar/', views.editar_comentario, name='editar'),
    
    # Excluir (soft delete) comentário
    path('<int:comentario_id>/excluir/', views.excluir_comentario, name='excluir'),
    
    # Listar comentários ativos de um anime
    path('anime/<int:anime_id>/lista/', views.listar_comentarios_anime, name='lista_por_anime'),
    
    # Listar comentários do usuário logado (com paginação)
    path('meus-comentarios/', views.meus_comentarios, name='meus_comentarios'),
]

