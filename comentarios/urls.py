from django.urls import path
from . import views

app_name = 'comentarios'

urlpatterns = [
    # Criar comentário
    path('anime/<int:anime_id>/criar/', views.criar_comentario, name='criar'),
    
    # Editar comentário
    path('<int:comentario_id>/editar/', views.editar_comentario, name='editar'),
    
    # Excluir comentário
    path('<int:comentario_id>/excluir/', views.excluir_comentario, name='excluir'),
    
    # Listar comentários de um anime
    path('anime/<int:anime_id>/lista/', views.listar_comentarios_anime, name='lista_por_anime'),
]
