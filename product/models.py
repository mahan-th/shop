from django.db import models
from django.utils.text import slugify

# Create your models here.
import os 
import random

def upload_to_image(instance,filename):
    exe = os.path.splitext(filename)[1]
    random_number = str(random.randint(1000,99999))
    return f"product/image/{random_number}.{exe}"


class Product(models.Model):

    title = models.CharField(max_length=100)

    price = models.IntegerField()

    final_price = models.IntegerField(default=0)
    
    discount = models.IntegerField(default=0)

    descriptions = models.TextField(blank=True)

    creat_at = models.DateTimeField(auto_now=True)

    is_avalible = models.BooleanField(default=True)

    image = models.ImageField(upload_to=upload_to_image)

    slug = models.SlugField(unique=True,blank=True)

    def __str__(self):
        return f"{self.title}"
    
    def save(self,*args,**kwargs):
        self.final_price = int(self.price - (self.price * self.discount/100))
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args,**kwargs)
    


class AttrbiuteProduct(models.Model):
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)


    def __str__(self):
        return f"products | {self.product.title}"
    
class ProductImage(models.Model):
    image = models.ImageField(upload_to=upload_to_image)
    product =  models.ForeignKey(Product,on_delete=models.CASCADE, related_name="images")


class ProdctPakage(models.Model):
    coler = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    is_avalable = models.BooleanField(default=True)

    def save(self,*args,**kwargs):
        self.product.final_price = int(self.product.price + self.price)
        return super().save(*args,**kwargs)
    



    