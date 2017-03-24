from .models import Node
from author.models import Author
import urllib
import json


def create_remote_author(host, uuid):
    host_model = Node.objects.get(url=host)

    if host_model.trusted:
        author = request_author(host, uuid)
        return author


def request_author(uuid, host):
    full_path = host + uuid
    response = urllib.request.urlopen(full_path).read()
    json_author = json.loads(response)
    return build_author(json_author)


def build_author(json_author):
    author = Author(
        displayName=json_author["displayName"],
        gitURL=json_author["gitURL"]
    )
    author.save()
    return author
