from django.contrib import admin
from post.models import *

# Register admin models for admin interface
class PostAdmin(admin.ModelAdmin):
    fields = ('author', 'content', 'privacyLevel', 'publishDate',
              'image_url', 'title', 'apiID', 'serverOnly',
              'source', 'origin', 'contentType', 'description',
              'categories', 'unlisted')

# Register your models here.
admin.site.register(Post, PostAdmin)
