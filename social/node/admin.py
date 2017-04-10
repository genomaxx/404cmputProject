from django.contrib import admin
from node.models import Node


class NodeAdmin(admin.ModelAdmin):
    fields = (
        'url',
        'trusted',
        'send_posts',
        'send_images',
        'username',
        'password',
        'user'
    )


admin.site.register(Node, NodeAdmin)
