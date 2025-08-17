from django.db import models
from django.utils.text import slugify

# Create your models here.
import os 
import random

def upload_to_image(instance,filename):
    exe = os.path.splitext(filename)[1]
    random_number = str(random.randint(1000,99999))
    return f"product/image/{random_number}.{exe}"


class Article(models.Model):

    title = models.CharField(max_length=400)

    descriptions = models.TextField()

    creat_at = models.DateTimeField(auto_now=True)

    update_at = models.DateTimeField(auto_now_add=True)

    image = models.ImageField(upload_to=upload_to_image)

    slug = models.SlugField(unique=True,blank=True)



class Attribut(models.Model):

    name = models.CharField(max_length=400)

    value = models.TextField()

    image = models.ImageField(upload_to=upload_to_image)

    article = models.ForeignKey(Article,on_delete=models.CASCADE)


