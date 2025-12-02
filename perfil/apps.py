from django.apps import AppConfig


class PerfilConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'perfil'
    verbose_name = 'Perfil'

    def ready(self):
        """Importar signals quando o app está pronto"""
        import perfil.models  # noqa
