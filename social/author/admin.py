from django.contrib import admin
from author.models import Follow, Author

# Register admin models for admin interface


class AuthorAdmin(admin.ModelAdmin):
    fields = ('id', 'friend', 'firstname', 'lastname','phone', 'dob', 'gitURL', 'gender')


class FollowAdmin(admin.ModelAdmin):
    fields = ('follower', 'followee')


# Register your models here.
admin.site.register(Author, AuthorAdmin)
admin.site.register(Follow, FollowAdmin)
