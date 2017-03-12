from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from api import views

urlpatterns = [
    url(r'^post/', views.getAllPosts),
    ]