from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from api import views

urlpatterns = [
    url(r'^posts/$', views.getAllPosts),
    url(r'^author/posts/$', views.getPosts),
    url(r'^author/(?P<id>[0-9a-f-]+)/$', views.getProfile),
    url(r'^posts/(?P<id>[0-9a-f-]+)/comments/$', views.getComments),
    url(r'^posts/(?P<id>[0-9a-f-]+)/$', views.getSinglePost),
    url(r'^author/(?P<id>[0-9a-f-]+)/friends/$', views.getFriends),
    url(r'^friendrequest/$', views.getFriendRequests),
    url(r'^author/(?P<id1>[0-9a-f-]+)/friends/(?P<id2>[0-9a-f]+)/$', views.checkFriends2),
    url(r'^author/(?P<id>[0-9a-f-]+)/posts/$', views.getAuthorPosts),
    ]
