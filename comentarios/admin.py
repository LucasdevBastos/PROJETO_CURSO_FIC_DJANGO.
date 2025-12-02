from django.contrib import admin
from .models import Comentario


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('user', 'anime_id', 'nota', 'criado_em')
    list_filter = ('criado_em', 'nota', 'user')
    search_fields = ('user__username', 'anime_id', 'texto')
    readonly_fields = ('criado_em', 'atualizado_em')
    fieldsets = (
        ('Informações', {
            'fields': ('user', 'anime_id', 'texto', 'nota')
        }),
        ('Datas', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )
