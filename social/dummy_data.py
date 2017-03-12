from django.contrib.auth.models import User
from author.models import Author
from post.models import Post


u1 = User(name="t1", password="t", email="t1@test.com")
u2 = User(name="t2", password="t", email="t2@test.com")
u1.save()
u2.save()

a1 = Author(id=u1, displayName="t1")
a2 = Author(id=u1, displayName="t1")
a1.save()
a2.save()

p1 = Post(content="Hello World", author=a1)
p2 = Post(content="Hello World Again", author=a2)
p1.save()
p2.save()
