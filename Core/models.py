from unittest.util import _MAX_LENGTH
from django.db import models
from SupperUserApp.models import Product

# Create your models here.

class HomeCategory(models.Model):
    HomeCategoryName=models.CharField(max_length=200)
    HomeCategorySlug=models.SlugField(blank=True, null=True, unique=True)


class HomeSubCategory(models.Model):
    ProductId=models.ForeignKey(to=Product,on_delete=models.CASCADE)
    HomeCategory=models.ForeignKey(to=HomeCategory,on_delete=models.CASCADE)
    # slug=models.SlugField(max_length = 200, null=True, blank=True, unique=True)

    
class Homebannerlist(models.Model):
    BannerTitle=models.CharField(max_length=200)
    BannerDiscount=models.CharField(max_length=200)
    BannerSubtitle=models.CharField(max_length=200)
    BannerBackgroundimg=models.ImageField(upload_to="Homebannerlist",null=True, blank=True)
    Bannersideimg=models.ImageField(upload_to="Homebannerlist",null=True, blank=True)

    def __str__(self):
        return self.BannerTitle

class BollyWoodCategory(models.Model):
    TagLine=models.TextField(blank=True)
    SubTagLine=models.TextField(null=True,blank=True)
    MainImage=models.ImageField(upload_to='BollywoodMainImage', null=True, blank=True)   
    BollyWoodCategorySlug=models.SlugField(blank=True, null=True, unique=True)

class BollyWoodSubCategory(models.Model):
    BollyWoodCategoryName=models.CharField(max_length=200,null=True, blank=True)
    ProductDetails=models.ForeignKey(to=Product, on_delete=models.CASCADE)
