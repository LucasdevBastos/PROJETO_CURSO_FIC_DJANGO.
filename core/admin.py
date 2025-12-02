from django.contrib import admin
from .models import Favorito, AnimeSyncStatus, SearchLog


@admin.register(Favorito)
class FavoritoAdmin(admin.ModelAdmin):
    list_display = ('user', 'anime_id', 'criado_em')
    list_filter = ('criado_em', 'user')
    search_fields = ('user__username', 'anime_id')
    readonly_fields = ('criado_em',)


@admin.register(AnimeSyncStatus)
class AnimeSyncStatusAdmin(admin.ModelAdmin):
    list_display = ('anime', 'last_synced_at')
    search_fields = ('anime__titulo',)


@admin.register(SearchLog)
class SearchLogAdmin(admin.ModelAdmin):
    list_display = ('termo_busca', 'executado_em')
    list_filter = ('executado_em',)
    search_fields = ('termo_busca',)
    readonly_fields = ('executado_em',)
