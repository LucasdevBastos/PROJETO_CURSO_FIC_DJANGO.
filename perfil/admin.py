from django.contrib import admin
from .models import Perfil


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'criado_em', 'atualizado_em')
    search_fields = ('user__username', 'user__email', 'bio')
    readonly_fields = ('criado_em', 'atualizado_em', 'user')
    fieldsets = (
        ('Usuário', {
            'fields': ('user',)
        }),
        ('Perfil', {
            'fields': ('avatar', 'bio')
        }),
        ('Datas', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )
