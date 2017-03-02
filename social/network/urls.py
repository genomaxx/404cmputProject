from django.conf.urls import url
from . import views

# Tells django which Python code handles which URL on the site.

urlpatterns = [
	url(r'^$', views.index, name='index'),
]
