# comments/models.py
from django.conf import settings
from django.db import models

from anime.models import Anime


class Comentario(models.Model):
    anime = models.ForeignKey(
        Anime,
        on_delete=models.CASCADE,
        related_name="comentarios",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comentarios",
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="respostas",
    )

    texto = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_editado = models.BooleanField(default=False)
    is_deletado = models.BooleanField(default=False)
    deletado_por_admin = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Comentário"
        verbose_name_plural = "Comentários"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Comentário de {self.user} em {self.anime}"


class ComentarioLike(models.Model):
    comentario = models.ForeignKey(
        Comentario,
        on_delete=models.CASCADE,
        related_name="likes",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comentario_likes",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Like em comentário"
        verbose_name_plural = "Likes em comentários"
        unique_together = ("comentario", "user")

    def __str__(self):
        return f"{self.user} curtiu {self.comentario_id}"


class ComentarioReport(models.Model):
    MOTIVO_OFENSIVO = "OFENSIVO"
    MOTIVO_SPAM = "SPAM"
    MOTIVO_OUTRO = "OUTRO"

    MOTIVOS = [
        (MOTIVO_OFENSIVO, "Ofensivo"),
        (MOTIVO_SPAM, "Spam"),
        (MOTIVO_OUTRO, "Outro"),
    ]

    STATUS_PENDENTE = "PENDENTE"
    STATUS_EM_ANALISE = "EM_ANALISE"
    STATUS_RESOLVIDO = "RESOLVIDO"

    STATUS = [
        (STATUS_PENDENTE, "Pendente"),
        (STATUS_EM_ANALISE, "Em análise"),
        (STATUS_RESOLVIDO, "Resolvido"),
    ]

    comentario = models.ForeignKey(
        Comentario,
        on_delete=models.CASCADE,
        related_name="reports",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comentario_reports",
    )
    motivo = models.CharField(max_length=20, choices=MOTIVOS)
    descricao = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default=STATUS_PENDENTE)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="comentario_reports_reviewed",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Denúncia de comentário"
        verbose_name_plural = "Denúncias de comentários"

    def __str__(self):
        return f"Report de {self.user} em {self.comentario_id}"
