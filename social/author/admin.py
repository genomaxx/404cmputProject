from django.contrib import admin
from author.models import Follow, Author

# Register admin models for admin interface


class AuthorAdmin(admin.ModelAdmin):
    fields = ('id', 'approved', 'firstname',
              'lastname','phone', 'dob', 'github', 
              'gender', 'host', 'displayName',
              'url', 'apiID', 'node', 'visibility')


class FollowAdmin(admin.ModelAdmin):
    fields = ('follower', 'followee')


# Register your models here.
admin.site.register(Author, AuthorAdmin)
admin.site.register(Follow, FollowAdmin)
