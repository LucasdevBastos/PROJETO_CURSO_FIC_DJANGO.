from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Comentario(models.Model):
    """Modelo para comentários de usuários sobre animes"""
    anime_id = models.IntegerField(help_text="ID do anime no MyAnimeList")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comentarios_anime')
    texto = models.TextField(max_length=2000, help_text="Texto do comentário (máx 2000 caracteres)")
    nota = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Nota de 1 a 10 (opcional)"
    )
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Comentário'
        verbose_name_plural = 'Comentários'
        ordering = ['-criado_em']
        indexes = [
            models.Index(fields=['anime_id', '-criado_em']),
            models.Index(fields=['user', '-criado_em']),
        ]

    def __str__(self):
        return f"Comentário de {self.user.username} sobre anime {self.anime_id}"
