from django.contrib import admin
from .models import Perfil


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'avatar_choice', 'is_vip', 'criado_em', 'atualizado_em')
    list_filter = ('is_vip', 'avatar_choice', 'criado_em')
    search_fields = ('user__username', 'user__email', 'bio')
    readonly_fields = ('criado_em', 'atualizado_em')
    
    fieldsets = (
        ('Usuário', {
            'fields': ('user', 'is_vip')
        }),
        ('Avatar', {
            'fields': ('avatar_choice', 'custom_avatar', 'avatar'),
            'description': 'Avatar padrão disponível para todos. Campos personalizados apenas para VIP.'
        }),
        ('Banner VIP', {
            'fields': ('custom_banner',),
            'classes': ('collapse',),
            'description': 'Banner personalizado disponível apenas para usuários VIP.'
        }),
        ('Sobre', {
            'fields': ('bio',)
        }),
        ('Datas', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        """
        Torna campos personalizados readonly se o usuário não for VIP
        """
        readonly = list(self.readonly_fields)
        if obj and not obj.is_vip:
            readonly.extend(['custom_avatar', 'custom_banner'])
        return readonly

