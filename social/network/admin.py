from django.contrib import admin
from network.models import *

# Register your models here.
myModels = [Author,Post,Comment,Follow]

admin.site.register(myModels)
