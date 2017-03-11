"""social URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from . import views
from author.views import author_image

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/', views.register, name='register'),
    url(r'^login/', views.login, name='login'),
    url(r'^admin/', admin.site.urls),
    url(r'^author/', include('author.urls', namespace='author')),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^post/', include('post.urls', namespace='post')),
    url(r'^service/', include('api.urls', namespace='api')),
    url(r'^images/(?P<pk>[0-9]+)/(?P<pk1>[._/0-9a-zA-Z]+)$', author_image, name='image'),
]
