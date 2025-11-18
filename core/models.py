# core/models.py
from django.db import models

from anime.models import Anime, Temporada


class AnimeSyncStatus(models.Model):
    anime = models.OneToOneField(
        Anime,
        on_delete=models.CASCADE,
        related_name="sync_status",
    )
    last_synced_at = models.DateTimeField(null=True, blank=True)
    last_payload = models.JSONField(default=dict, blank=True)
    etag = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = "Status de sincronização do anime"
        verbose_name_plural = "Status de sincronização dos animes"

    def __str__(self):
        return f"Sync {self.anime} em {self.last_synced_at}"


class SyncLog(models.Model):
    SOURCE_MAL = "MAL"

    SOURCE_CHOICES = [
        (SOURCE_MAL, "MyAnimeList"),
    ]

    TIPO_FULL = "FULL_IMPORT"
    TIPO_TEMPORADA = "ATUALIZAR_TEMPORADA"
    TIPO_ANIME = "ATUALIZAR_ANIME"

    TIPOS = [
        (TIPO_FULL, "Importação completa"),
        (TIPO_TEMPORADA, "Atualizar temporada"),
        (TIPO_ANIME, "Atualizar anime"),
    ]

    STATUS_SUCESSO = "SUCESSO"
    STATUS_ERRO = "ERRO"

    STATUS_CHOICES = [
        (STATUS_SUCESSO, "Sucesso"),
        (STATUS_ERRO, "Erro"),
    ]

    source = models.CharField(max_length=10, choices=SOURCE_CHOICES, default=SOURCE_MAL)
    tipo = models.CharField(max_length=30, choices=TIPOS)
    temporada = models.ForeignKey(
        Temporada,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sync_logs",
    )

    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    mensagem = models.TextField(blank=True)
    qtd_animes_atualizados = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Log de sincronização"
        verbose_name_plural = "Logs de sincronização"
        ordering = ["-started_at"]

    def __str__(self):
        return f"[{self.get_status_display()}] {self.get_tipo_display()} - {self.started_at:%d/%m/%Y}"


class SearchLog(models.Model):
    termo_busca = models.CharField(max_length=255)
    filtros = models.JSONField(default=dict, blank=True)
    executado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Log de busca"
        verbose_name_plural = "Logs de busca"
        ordering = ["-executado_em"]

    def __str__(self):
        return self.termo_busca
