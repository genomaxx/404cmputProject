from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import posts

urlpatterns = [
    url(r'^post/', posts.getAllPosts, name='getAllPosts'),

    ]