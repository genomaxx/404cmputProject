from django.contrib import admin
from .models import Settings

# Register your models here.


class SettingsAdmin(admin.ModelAdmin):

    fields = ('auth_required', 'send_images', 'send_posts')

    def __str__(self):
        return "Settings"


admin.site.register(Settings, SettingsAdmin)
