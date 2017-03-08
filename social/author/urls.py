from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^author_post/', views.author_post, name='author_post'),
    url(r'^profile/', views.profile, name='profile'),
    url(r'^$', views.index, name='index'),
]