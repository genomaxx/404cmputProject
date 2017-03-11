from django.http import HttpResponse, JsonResponse

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework import authentication, permissions, status
from rest_framework.response import Response


from post.models import Post
from api.serializers import PostSerializer

'''
Follow the tutorial online if you get lost:
http://www.django-rest-framework.org/

Authentication (use BasicAuth and SessionAuth):
http://www.django-rest-framework.org/api-guide/authentication/

REST Response:
http://www.django-rest-framework.org/api-guide/responses/

REST Status Codes:
http://www.django-rest-framework.org/api-guide/status-codes/
'''

@api_view(['GET'])
@permission_classes((IsAuthenticated))
@authentication_classes((SessionAuthentication, BasicAuthentication))
def getAllPosts(request):
    # HTTP request is not a GET
    if (request.method != 'GET'):
        return Response('GET requests only', status=status.HTTP_400_BAD_REQUEST)

    query = Post.objects.filter(
        privacyLevel=0).order_by('-publishDate')
    if (len(query) > 0):
        serialize = PostSerializer(query, many=True)
        return Response(serialize.data)

    return Response('No posts found', status=status.HTTP_200_OK)




