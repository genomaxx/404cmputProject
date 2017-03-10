from django.contrib import admin
from author.models import Author

# Register admin models for admin interface


class AuthorAdmin(admin.ModelAdmin):
    fields = ('id', 'friend')


# Register your models here.
admin.site.register(Author, AuthorAdmin)
