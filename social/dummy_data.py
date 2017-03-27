from django.contrib.auth.models import User
from author.models import Author
from node.models import Node


u1 = User.objects.create_user("usera", "usera@usera.com", "usera")
u1.save()

a1 = Author.objects.create(
    id=u1
)
a1.approved = True
a1.save()

n1 = Node(
    url="http://foundbook.herokuapp.com/",
    user=u1,
    username="fishy123",
    password="not_a_fish",
    trusted=True
)

n1.save()

User.objects.create_superuser(
    username="admin",
    email="admin@admin.com",
    password="iamthebestadmin"
)
