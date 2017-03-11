from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^author_post/', views.author_post, name='author_post'),
    url(r'^author_delete_post/(?P<postpk>[0-9]+)$', views.author_delete_post, name='author_delete_post'),
    url(r'^edit/', views.edit, name='edit'),
    url(r'^(?P<id>[0-9]+)/$', views.profile, name='profile'),
    url(r'edit_post/', views.edit_post, name='edit_post'),
    url(r'^$', views.index, name='index'),
]
