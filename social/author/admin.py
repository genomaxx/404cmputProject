from django.contrib import admin
from author.models import *

# Register admin models for admin interface
class AuthorAdmin(admin.ModelAdmin):
    fields = ('user', 'friend')

# Register your models here.
admin.site.register(Author, AuthorAdmin)
