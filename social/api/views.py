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
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework import authentication, permissions, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
# App
from post.models import Post
from node.models import Node
from comment.models import Comment
from author.models import Author, Follow
from node.models import *
from api.serializer import PostSerializer, AuthorSerializer, UserSerializer, CommentSerializer
from api.paginator import CustomPagination
from collections import OrderedDict
import uuid
import json
from .auth import APIAuthentication
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
@api_view(['GET'])
@permission_classes((APIAuthentication,))
@authentication_classes((SessionAuthentication, BasicAuthentication))
def getAllPosts(request):
    ###########
    # NOTE: The decorator automatically checks for you. Error reponse is 405
    # I'm keeping this here as a reminder while we build out the API
    ############
    paginator = PageNumberPagination()
    query = Post.objects.filter(
        Q(privacyLevel=0) &
        Q(serverOnly=False)).filter(origin__startswith='http://polar-savannah-14727').order_by('-publishDate')

    if (len(query) > 0):
        try:
            paginated = paginator.paginate_queryset(query, request)
            response = PostSerializer(paginated, many=True, context=request)
            return paginator.get_paginated_response(response.data)
        except:
            return Response('Request failure', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response('No posts found', status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes((APIAuthentication,))
@authentication_classes((SessionAuthentication, BasicAuthentication))
def getProfile(request, id):
    try:
        query = Author.objects.get(UID=id)
    except:
        return Response("No author exists with id " + id, status=status.HTTP_404_NOT_FOUND)

    if (query != None): # Check if there is a result
        try:
            response = AuthorSerializer(query, context='profile')
            return Response(response.data)
        except Exception as e:
            return Response('Request failure', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response('No author found', status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
@permission_classes((APIAuthentication,))
@authentication_classes((SessionAuthentication, BasicAuthentication))
def getComments(request, id):

    # Add a comment
    if (request.method == 'POST'):
        return addComment(request, id)

    post = checkForPost(id)
    if (post == None):
        return postIsServerOnlyOrNone()

    query = Comment.objects.filter(post__UID=id)
    paginator = CustomPagination()
    if (len(query) > 0):
        try:
            paginated = paginator.paginate_queryset(query, request)
            response = CommentSerializer(paginated, many=True)
            return paginator.get_paginated_response(response.data, request)
        except Exception as e:
            return Response('Request failure', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response('No comments found for post ID ' + str(id), status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes((APIAuthentication,))
@authentication_classes((SessionAuthentication, BasicAuthentication))
def getSinglePost(request, id):
    try:
        query = Post.objects.get(Q(UID=id) & 
                                 Q(serverOnly=False))
    except:
        return Response('No post found for post ID ' + str(id), status=status.HTTP_404_NOT_FOUND)

    if (query != None):
        try:
            response = PostSerializer(query, context=request)
            return Response(response.data)
        except Exception as e:
            return Response('Request failure', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response('No post found for post ID ' + str(id), status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes((APIAuthentication,))
@authentication_classes((SessionAuthentication, BasicAuthentication))
def getFriends(request, id):
    try:
        author = Author.objects.get(UID=id)
    except:
        return Response('No author found with id ' + str(id), status=status.HTTP_404_NOT_FOUND)

    query = author.getFriends()
    if (len(query) == 0):
        return Response('No friends found for author ' + str(id), status=status.HTTP_404_NOT_FOUND)

    response = OrderedDict([
        ('authors',[])
        ])
    for auth in query:
        response['authors'].append(str(auth.UID))

    return Response(response, status=status.HTTP_200_OK)


def addComment(request, postId):
    try:
        post = checkForPost(id)
        if (post == None):
            return postIsServerOnlyOrNone()
        #post = Post.objects.get(UID=postId)
        #if (post == None):
        #    return Response('No post with the id ' + postId + ' exists', status=status.HTTP_400_BAD_REQUEST)
        build_comment(request.data['comment'], post)
    except Exception as e:
        return Response('Request failure', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(successResponse('addComment', 'Comment Added'), status=status.HTTP_200_OK)

def checkForPost(id):
    post = Post.objects.filter(Q(UID=id) &
                               Q(serverOnly=False))
    return post

def postIsServerOnlyOrNone():
    return Response('Post is either private to server or none was found', status=status.HTTP_400_BAD_REQUEST)

def successResponse(query, msg):
   return OrderedDict ([
        ('query', query),
        ('success', True),
        ('message', msg)
        ])


@api_view(['POST'])
@permission_classes((APIAuthentication,))
@authentication_classes((SessionAuthentication, BasicAuthentication))
def getFriendRequests(request):
    the_json = json.loads(request.body)
    followee_id = uuid.UUID(the_json["author"]["id"])
    follower_host = uuid.UUID(the_json["friend"]["host"])
    follower_url = uuid.UUID(the_json["friend"]["url"])
    node = Node.objects.get(url=follower_host)
    friend = node.get_author(follower_url)
    try:
        follower = Author.objects.get(UID=followee_id)
    except:
        return Response('No author found with id ' + str(id), status=status.HTTP_404_NOT_FOUND)
    followee = friend
    Follow(follower=follower, followee=followee).save()

    response = {
        "query": "friendrequest",
        "message": "Request Completed",
        "success": True
    }

    return Response(json.dumps(response), status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((APIAuthentication,))
@authentication_classes((SessionAuthentication, BasicAuthentication))
def getPosts(request):
    ###########
    # NOTE: The decorator automatically checks for you. Error reponse is 405
    # I'm keeping this here as a reminder while we build out the API
    ############
    paginator = PageNumberPagination()
    query = Post.objects.exclude(privacyLevel=5).exclude(privacyLevel=4).exclude(serverOnly=True).filter(origin__startswith='http://polar-savannah-14727').order_by('-publishDate')

    if (len(query) > 0):
        try:
            paginated = paginator.paginate_queryset(query, request)
            response = PostSerializer(paginated, many=True, context=request)
            return paginator.get_paginated_response(response.data)
        except:
            return Response('Request failure', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response('No posts found', status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes((APIAuthentication,))
@authentication_classes((SessionAuthentication, BasicAuthentication))
def getAuthorPosts(request, id):
    ###########
    # NOTE: The decorator automatically checks for you. Error reponse is 405
    # I'm keeping this here as a reminder while we build out the API
    ############
    paginator = PageNumberPagination()
    try:
        author = Author.objects.get(UID=id)
    except:
         return Response('No author found with id ' + str(id), status=status.HTTP_404_NOT_FOUND)

    query = Post.objects.filter(author=author).exclude(privacyLevel=5).exclude(privacyLevel=4).exclude(serverOnly=True).filter(origin__startswith='http://polar-savannah-14727').order_by('-publishDate')

    if (len(query) > 0):
        try:
            paginated = paginator.paginate_queryset(query, request)
            response = PostSerializer(paginated, many=True, context=request)
            return paginator.get_paginated_response(response.data)
        except:
            return Response('Request failure', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response('No posts found', status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes((APIAuthentication,))
@authentication_classes((SessionAuthentication, BasicAuthentication))
def checkFriends2(request, id1, id2):
    try:
        author1 = Author.objects.get(UID=id1)
    except:
         return Response('No author found with id ' + str(id), status=status.HTTP_404_NOT_FOUND)

    try:
        author2 = Author.objects.get(UID=id2)
    except:
         return Response('No author found with id ' + str(id), status=status.HTTP_404_NOT_FOUND)

    response = OrderedDict([
        ('authors',[])
        ])

    response['authors'].append(str(id1))
    response['authors'].append(str(id2))

    if author1.isFriend(author2):
        response['friends'] = 'True'
    else:
        response['friends'] = 'False'

    return Response(response, status=status.HTTP_200_OK)
