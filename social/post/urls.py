from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<pk>[0-9]+)/$', views.PostView.as_view(), name='post'),
    url(r'^(?P<pk>[0-9]+)/comment/$', views.AddComment.as_view(), name='comment'),
    url(r'^(?P<pk>[0-9]+)/ajaxcomments/$', views.AjaxComments, name='ajax_comments'),
]
