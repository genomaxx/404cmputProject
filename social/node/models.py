from django.db import models


# Create your models here.
class Node(models.Model):

    url = models.CharField(max_length=128)
    trusted = models.BooleanField()
