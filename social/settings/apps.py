from django.apps import AppConfig


class SettingsConfig(AppConfig):
    name = 'settings'

    def ready(self):
        from .models import Settings
        settings, _ = Settings.objects.get_or_create(id=0)
        settings.save()
