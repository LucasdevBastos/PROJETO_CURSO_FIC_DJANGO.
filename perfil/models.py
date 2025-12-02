from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import os


class Perfil(models.Model):
    """Modelo para perfil do usuário"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    avatar = models.ImageField(
        upload_to="avatars/%Y/%m/",
        null=True,
        blank=True,
        help_text="Avatar do usuário (recomendado: 200x200px)"
    )
    bio = models.TextField(
        blank=True,
        max_length=500,
        help_text="Biografia do usuário (máx 500 caracteres)"
    )
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'

    def __str__(self):
        return f"Perfil de {self.user.username}"

    def get_avatar_url(self):
        """Retorna URL do avatar ou uma imagem padrão"""
        if self.avatar:
            return self.avatar.url
        return 'https://ui-avatars.com/api/?name=' + self.user.first_name.replace(' ', '+')


@receiver(post_save, sender=User)
def criar_perfil_usuario(sender, instance, created, **kwargs):
    """
    Sinal para criar automaticamente um perfil quando um usuário é criado
    """
    if created:
        Perfil.objects.create(user=instance)


@receiver(post_save, sender=User)
def salvar_perfil_usuario(sender, instance, **kwargs):
    """
    Sinal para salvar o perfil quando um usuário é salvo
    """
    if hasattr(instance, 'perfil'):
        instance.perfil.save()
