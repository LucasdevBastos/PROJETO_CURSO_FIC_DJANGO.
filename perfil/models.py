from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import os


class Perfil(models.Model):
    """Modelo para perfil do usuário"""
    
    # Choices para avatares padrão
    AVATAR_CHOICES = [
        ('avatar_1.jpg', 'Avatar 1'),
        ('avatar_2.jpg', 'Avatar 2'),
        ('avatar_3.jpg', 'Avatar 3'),
        ('avatar_4.jpg', 'Avatar 4'),
        ('avatar_5.jpg', 'Avatar 5'),
        ('avatar_6.jpg', 'Avatar 6'),
        ('avatar_7.jpg', 'Avatar 7'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    
    # Sistema de avatares padrão (disponível para todos)
    avatar_choice = models.CharField(
        max_length=20,
        choices=AVATAR_CHOICES,
        default='avatar_1.jpg',
        verbose_name='Avatar Padrão',
        help_text='Escolha um dos avatares padrão disponíveis'
    )
    
    # Campo VIP
    is_vip = models.BooleanField(
        default=False,
        verbose_name='É VIP',
        help_text='Marca se o usuário tem privilégios VIP (avatar/banner personalizados)'
    )
    
    # Campos personalizados (apenas para VIP)
    custom_avatar = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='Avatar Personalizado',
        help_text='URL ou caminho do avatar personalizado (apenas VIP)'
    )
    
    custom_banner = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='Banner Personalizado',
        help_text='URL ou caminho do banner personalizado (apenas VIP)'
    )
    
    # Campo legacy (manter por compatibilidade)
    avatar = models.ImageField(
        upload_to="avatars/%Y/%m/",
        null=True,
        blank=True,
        help_text="Avatar do usuário (recomendado: 200x200px) - DEPRECATED: use avatar_choice"
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
        """
        Retorna URL do avatar seguindo a prioridade:
        1. Se VIP e tem custom_avatar, usa custom_avatar
        2. Caso contrário, usa avatar padrão da pasta static/avatars/
        3. Fallback para avatar legacy (campo ImageField antigo)
        """
        if self.is_vip and self.custom_avatar:
            return self.custom_avatar
        
        # Avatar padrão da pasta static/avatars/
        if self.avatar_choice:
            return f'/static/avatars/{self.avatar_choice}'
        
        # Fallback para avatar legacy
        if self.avatar:
            return self.avatar.url
        
        # Fallback final
        return f'/static/avatars/avatar_1.jpg'
    
    def get_banner_url(self):
        """
        Retorna URL do banner (apenas para VIP)
        """
        if self.is_vip and self.custom_banner:
            return self.custom_banner
        return None
    
    def save(self, *args, **kwargs):
        """
        Override do save para garantir regras VIP:
        - Apenas VIP pode ter custom_avatar e custom_banner
        - Se não for VIP, limpa esses campos
        """
        if not self.is_vip:
            self.custom_avatar = None
            self.custom_banner = None
        super().save(*args, **kwargs)


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
