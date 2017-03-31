from django.contrib import admin
from node.models import Node


class NodeAdmin(admin.ModelAdmin):
    fields = ('url', 'trusted', 'username', 'password', 'user')


admin.site.register(Node, NodeAdmin)
