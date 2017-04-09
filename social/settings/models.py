from django.db import models


class Settings(models.Model):
    auth_required = models.BooleanField(
        default=True,
        verbose_name="Node Authentication"
    )
    send_images = models.BooleanField(
        default=True,
        verbose_name="Send images to nodes"
    )
    send_posts = models.BooleanField(
        default=True,
        verbose_name="Send posts to nodes"
    )

    class Meta:
        verbose_name_plural = "Settings"

    def __str__(self):
        return "Settings"
