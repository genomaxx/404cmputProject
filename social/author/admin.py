from django.contrib import admin
from author.models import *

# Register admin models for admin interface
class AuthorAdmin(admin.ModelAdmin):
    fields = ('id', 'user', 'friend')

# Register your models here.
models = [Author, AuthorAdmin]
admin.site.register(Author, AuthorAdmin)