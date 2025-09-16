from django.db import models
from django.utils.text import slugify
from django.db.models import F,ExpressionWrapper,DecimalField
from django.db.models.signals import post_save , post_delete
from django.dispatch import receiver
from django.db.models import Min
import os 
import random

def upload_to_image(instance,filename):
    exe = os.path.splitext(filename)[1]
    random_number = str(random.randint(1000,99999))
    return f"product/image/{random_number}.{exe}"


class Product(models.Model):

    title = models.CharField(max_length=100)

    descriptions = models.TextField(blank=True)

    image = models.ImageField(upload_to=upload_to_image)

    price = models.IntegerField(default=0)

    discount = models.IntegerField(default=0)

    final_price = models.IntegerField(default=0)

    creat_at = models.DateTimeField(auto_now=True)

    categories = models.ManyToManyField("Category",related_name='categories')
    
    slug = models.SlugField(unique=True,blank=True, max_length=500 ,allow_unicode=True)

    def __str__(self):
        return f"{self.title}"
    
    def save(self,*args,**kwargs):

        self.final_price = int(self.price - (self.price * self.discount/100))
        if not self.slug:
            self.slug = slugify(self.title,allow_unicode=True)
            
        return super().save(*args,**kwargs)

   
class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True ,blank=True, allow_unicode=True)
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="children")

    def __str__(self):
        return f'Category |{self.title}'

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(self.title,allow_unicode=True)
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

    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="packages")

    coler = models.CharField(max_length=50)

    coler_hex = models.CharField(max_length=300)

    price = models.IntegerField(default=0)

    final_price = models.IntegerField(default=0)

    discount = models.IntegerField(default=0)

    is_avalable = models.BooleanField(default=True)
     
    product_number = models.IntegerField(default=0)


    def save(self,*args,**kwargs):

        self.final_price = int(self.price - (self.price * self.discount/100))

        super().save(*args,**kwargs)
        min_pakage = self.product.packages.aggregate(Min('final_price'))['final_price__min']
        if min_pakage != None and min_pakage != self.product.final_price:
            self.product.price = self.price
            self.product.discount = self.discount
            
            self.product.final_price = min_pakage
            self.product.save()






    


    