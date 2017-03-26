from django.contrib import admin
from node.models import Node


class NodeAdmin(admin.ModelAdmin):
    fields = ('url', 'trusted', 'username', 'password')


admin.site.register(Node, NodeAdmin)
