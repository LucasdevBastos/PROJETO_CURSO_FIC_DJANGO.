from django.urls import path
from . import views

app_name = 'perfil'

urlpatterns = [
    # Editar perfil do usuário logado (ANTES de <username>/)
    path('editar/', views.editar_perfil, name='editar'),
    
    # Todos os comentários de um usuário
    path('<str:username>/comentarios/', views.todos_comentarios_usuario, name='todos_comentarios'),
    
    # Todos os favoritos de um usuário
    path('<str:username>/favoritos/', views.todos_favoritos_usuario, name='todos_favoritos'),
    
    # Ver perfil de um usuário (DEPOIS das rotas específicas)
    path('<str:username>/', views.perfil_usuario, name='ver'),
]
