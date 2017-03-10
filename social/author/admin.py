from django.contrib import admin
from author.models import *

# Register admin models for admin interface
class AuthorAdmin(admin.ModelAdmin):
    fields = ('id', 'friend', 'firstname', 'lastname','phone', 'dob', 'gitURL', 'gender')

# Register your models here.
admin.site.register(Author, AuthorAdmin)
