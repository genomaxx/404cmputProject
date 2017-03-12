# Django
from django.http import HttpResponse
from django.core import serializers
from django.db.models import Q
# Django REST
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework import authentication, permissions, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
# App
from post.models import Post
from api.serializer import PostSerializer, AuthorSerializer, UserSerializer

'''
Follow the tutorial online if you get lost:
http://www.django-rest-framework.org/

Authentication (use BasicAuth and SessionAuth):
http://www.django-rest-framework.org/api-guide/authentication/

REST Response:
http://www.django-rest-framework.org/api-guide/responses/

REST Status Codes:
http://www.django-rest-framework.org/api-guide/status-codes/

Django Serialization:
https://docs.djangoproject.com/en/1.10/topics/serialization/
'''

# Create your views here.
class PublicPostListAPIView(APIView):
    query = Post.objects.filter(
           Q(privacyLevel=0)).order_by('-publishDate')
    serializer_class = PostSerializer(query, many=True)
    #print(serializer_class.data)

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((SessionAuthentication, BasicAuthentication))
def getAllPosts(request):
    ###########
    # NOTE: The decorator automatically checks for you. Error reponse is 405
    # I'm keeping this here as a reminder while we build out the API
    ############
    paginator = PageNumberPagination()
    query = Post.objects.filter(
        privacyLevel=0).order_by('-publishDate')

    if (len(query) > 0):
        try:
            paginated = paginator.paginate_queryset(query, request)
            response = PostSerializer(paginated, many=True)
            return paginator.get_paginated_response(response.data)
        except:
            return Response(response.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response('No posts found', status=status.HTTP_200_OK)