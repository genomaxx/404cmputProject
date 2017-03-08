from django.contrib import admin
from comment.models import *

# Register your models here.
class CommentAdmin(admin.ModelAdmin):
    fields = ('author', 'content', 'publishDate')

# Register your models here.
admin.site.register(Comment, CommentAdmin)
