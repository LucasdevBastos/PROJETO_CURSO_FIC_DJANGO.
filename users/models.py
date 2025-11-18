# users/models.py
from django.conf import settings
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    display_name = models.CharField("Nome público", max_length=150, blank=True)
    avatar_url = models.URLField("Avatar (URL)", blank=True)
    bio = models.TextField("Biografia", blank=True)
    preferencias = models.JSONField("Preferências", default=dict, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfis"

    def __str__(self):
        return self.display_name or self.user.get_username()


class Role(models.Model):
    """
    Papel no sistema: ADMIN, USER, MODERADOR, etc.
    """

    name = models.CharField("Nome", max_length=50, unique=True)
    descricao = models.TextField("Descrição", blank=True)

    class Meta:
        verbose_name = "Papel"
        verbose_name_plural = "Papéis"

    def __str__(self):
        return self.name


class UserRole(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_roles",
    )
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="user_roles")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Papel do usuário"
        verbose_name_plural = "Papéis dos usuários"
        unique_together = ("user", "role")

    def __str__(self):
        return f"{self.user} → {self.role}"
