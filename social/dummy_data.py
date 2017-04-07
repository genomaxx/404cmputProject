from django.contrib.auth.models import User
from author.models import Author
from node.models import Node


u1 = User.objects.create_user("usera", "usera@usera.com", "usera")
u1.save()

u2 = User.objects.create_user("group1", "group1@group1.com", "group1")
u2.save()

u3 = User.objects.create_user("userb","userb@userb.com","userb")
u3.save()

a1 = Author(id=u1)
a1.setDisplayName()
a1.setAuthorURL()
a1.setApiID()
a1.approved = True
a1.save()

n1 = Node(
     url="http://foundbook.herokuapp.com/",
     user=u1,
     username="fishy123",
     password="not_a_fish",
     trusted=True
)

n2 = Node(
     url="http://coolbear.herokuapp.com/",
     user=u2,
     username="group8",
     password="tester123",
     trusted=True
)

n3 = Node(
    url="",
    user=u3,
    username="",
    password="",
    trusted=True
)

n1.save()
n2.save()
n3.save()

User.objects.create_superuser(
    username="admin",
    email="admin@admin.com",
    password="iamthebestadmin"
)
