from distutils.command.upload import upload
from email.policy import default
import re
from unittest.util import _MAX_LENGTH
from xmlrpc.client import Boolean
from datetime import *
from django.db import models
from django.urls import reverse
from django.utils.html import format_html
from Accounts.models import Login
from ckeditor.fields import RichTextField
from django.core.validators import MaxLengthValidator, MinLengthValidator
from Accounts.models import *

# Create your models here.
class CategoryLevel1(models.Model):
    CategoryName=models.CharField(max_length=200)
    CategoryImage=models.ImageField(upload_to='CategoryLevel1')
    CategoryDescription=models.TextField(blank=True,null=True)
    CategorySlug= models.SlugField(max_length = 200, null=True, blank=True, unique=True)
    SubCategoryName=models.JSONField(null=True,blank=True)
    CategoryProductCount=models.IntegerField(null=True,blank=True)

    def __str__(self):
        return self.CategoryName

class CategoryLevel2(models.Model):
    CategoryLevel1Id=models.ForeignKey(to=CategoryLevel1,on_delete=models.SET_NULL,null=True,blank=True)
    CategoryLevel2Name=models.CharField(max_length=200, blank=True,null=True)
    CategoryImages=models.ImageField(upload_to='CategoryLevel2', default='',blank=True,null=True)
    CategoryDescription=models.TextField(blank=True,null=True)
    CategorySlug= models.SlugField(max_length = 200, null=True, blank=True, unique=True)
    
    def __str__(self):
        return self.CategoryLevel2Name

class CategoryLevel3(models.Model):
    CategoryLevel2Id=models.ForeignKey(to=CategoryLevel2,on_delete=models.SET_NULL,null=True,blank=True)
    CategoryLevel3Name=models.CharField(max_length=200)
    CategoryImages=models.ImageField(upload_to='CategoryLevel2', default='',blank=True,null=True)
    CategoryDescription=models.TextField(blank=True,null=True)
    CategorySlug= models.SlugField(max_length = 200, null=False, unique=True)
    productcount=models.IntegerField(null=True,blank=True,default=0)

    def __str__(self):
        return self.CategoryLevel3Name

    def get_absolute_url(self):
        return reverse("article_detail", kwargs={"slug": self.slug})

class Product(models.Model):
    CategoryLevel1Id=models.ForeignKey(to=CategoryLevel1,on_delete=models.SET_NULL,null=True,blank=True)
    CategoryLevel2Id=models.ForeignKey(to=CategoryLevel2,on_delete=models.SET_NULL,null=True,blank=True)
    CategoryLevel3Id=models.ForeignKey(to=CategoryLevel3,on_delete=models.SET_NULL,null=True,blank=True)
    ProductName=models.CharField(max_length=200)
    ProductDescription=models.TextField(blank=True,null=True)
    Star=models.FloatField(default=0, blank=True,null=True)
    TotalRatingCount=models.IntegerField(default=0, null=True,blank=True)
    TotalReviewCount=models.IntegerField(default=0, null=True,blank=True)   
    ProductSlug= models.SlugField(max_length = 200, null=True, blank=True, unique=True)
    ProductMainImage=models.ImageField(upload_to='ProductmainImage', null=True, blank=True, unique=True)
    ProductBrandName=models.CharField(max_length=200, null=True, blank=True)
    file1=models.ImageField(upload_to='file1', null=True, blank=True)
    file2=models.ImageField(upload_to='file2', null=True, blank=True)
    file3=models.ImageField(upload_to='file3', null=True, blank=True)
    file4=models.ImageField(upload_to='file4', null=True, blank=True)
    file5=models.ImageField(upload_to='file5', null=True, blank=True)
    file6=models.FileField(upload_to='file6', null=True, blank=True)
    TotalProduct=models.IntegerField(null=True, blank=True)
    Price = models.FloatField(blank=True,null=True)
    DiscountPercent = models.FloatField(default=0,blank=True,null=True)
    Product_Specification=RichTextField(null=True,blank=True,default=0)

    @property
    def discount(self):
        if self.DiscountPercent > 0:
            discounted_price = round(self.Price - self.Price * self.DiscountPercent / 100)
            return discounted_price

   
class ProductColor(models.Model):
    ProductColorName=models.CharField(max_length=200,null=True, blank=True)

    def __str__(self):
        return self.ProductColorName

class ProductColourImage(models.Model):
    ProductImageName=models.CharField(max_length=200,null=True)
    ProductColor=models.ForeignKey(to=ProductColor,on_delete=models.SET_NULL,null=True,blank=True)
    ProductColourImage=models.ImageField(upload_to='ProductColourImage', null=True, blank=True)

    def __str__(self):
        return self.ProductImageName

class ProductSize(models.Model):
    size = models.CharField(max_length=200)

    def __str__(self):
        return self.size
    
class ProductSizeColor(models.Model):
    Product=models.ForeignKey(to=Product,on_delete=models.SET_NULL,null=True)
    ProductColour=models.ForeignKey(to=ProductColor,on_delete=models.SET_NULL,null=True)
    ProductSize=models.ForeignKey(to=ProductSize,on_delete=models.SET_NULL,null=True)
    ProductImage=models.ImageField(upload_to="ProductColourImage",null=True,blank=True)
    Stock=models.IntegerField()
    Price = models.FloatField(blank=True,null=True)
    DiscountPercent = models.FloatField(default=0,blank=True,null=True)

    @property
    def discount(self):
        if self.DiscountPercent > 0:
            discounted_price = self.Price - self.Price * self.DiscountPercent / 100
            return discounted_price

    @property
    def saved(self):
        return self.Price-self.discount


    

class ProductSpecification(models.Model):
    Product=models.ForeignKey(to=Product,on_delete=models.SET_NULL,null=True)
    productDetail=models.JSONField(blank=True)


class AddToCart(models.Model):
    ProductSizeColorId=models.ForeignKey(to=ProductSizeColor, on_delete=models.CASCADE)
    LoginId=models.ForeignKey(to=Login, on_delete=models.CASCADE)
    DateTime=models.DateTimeField(auto_now_add=True)
    Qunatity=models.IntegerField()
    TotalPrice=models.FloatField()
    MoneyStatus=models.BooleanField(default=0)
    orderid=models.CharField(max_length=200, null=True, blank=True)
    razor_pay_order_id=models.CharField(max_length=200, null=True, blank=True)
    razor_pay_payment_id=models.CharField(max_length=200, null=True, blank=True)
    razor_pay_payment_signature=models.CharField(max_length=200, null=True, blank=True)
    
    OrderDate=models.DateField(null=True, blank=True)

    CancelledStatus=models.BooleanField(default=0, null=True, blank=True)
    CancelDate=models.DateField(null=True, blank=True)

    delivry_address=models.ForeignKey(to=Address,on_delete=models.CASCADE, null=True, blank=True)
    DeliveryStatus=models.BooleanField(default=0, null=True, blank=True)
    DeliveryDate=models.DateField(null=True, blank=True)
    ExtimateDeliveryAddress=models.DateField(null=True, blank=True)

    RefundStatus=models.BooleanField(default=0, null=True, blank=True)
    RefundDate=models.DateField(null=True, blank=True)


    Exchangedate=models.DateField(null=True, blank=True)
    ExchangeStatus=models.BooleanField(default=0, null=True, blank=True)

    ReturnrequestbyDate=models.DateField(null=True, blank=True)
    ReturnRequest=models.BooleanField(default=0, null=True, blank=True)
    
    ReturnrequestDate=models.DateField(null=True, blank=True)
    ReturnRequestStatus=models.BooleanField(default=0, null=True, blank=True)
    
    Payment_method=models.CharField(max_length=200, null=True, blank=True)
    

    def __str__(self):
        return str(self.MoneyStatus)


class Rating_Product(models.Model):
    Cart=models.ForeignKey(to=Product, on_delete=models.CASCADE)
    login_id=models.ForeignKey(to=Login, on_delete=models.CASCADE)
    Rating_star=models.IntegerField(default=0,validators=[MaxLengthValidator(5),MinLengthValidator(0)])
    
    

class Review_products(models.Model):
    Cart=models.ForeignKey(to=Product, on_delete=models.CASCADE)
    login_id=models.ForeignKey(to=Login, on_delete=models.CASCADE)
    Review=models.TextField(null=True, blank=True)
    Review_Date=models.DateField()
    Image1=models.FileField(upload_to='ReviewImage1', null=True, blank=True)
    Image2=models.FileField(upload_to='ReviewImage2', null=True, blank=True)
    likes = models.ManyToManyField(to=Login, blank=True, related_name='Review_likes')
    dislikes = models.ManyToManyField(to=Login, blank=True, related_name='Review_dislikes')


class QuestionsAndAnswers(models.Model):
    Question=models.TextField()
    Answer=models.TextField()
    Addedby=models.ForeignKey(to=Login, on_delete=models.CASCADE)
    Date=models.DateField(auto_now_add=True, blank=True)
    ProductId=models.ForeignKey(to=Product, on_delete=models.CASCADE, null= True, blank= True)
    likes = models.ManyToManyField(to=Login, blank=True, related_name='likes')
    dislikes = models.ManyToManyField(to=Login, blank=True, related_name='dislikes')


class Return_Product(models.Model):
    ProductId=models.ForeignKey(to=AddToCart, on_delete=models.CASCADE)
    login=models.ForeignKey(to=Login, on_delete=models.CASCADE)
    Reason=models.CharField(max_length=100, null=True, blank=True)
    Message=models.TextField(null=True, blank=True)
    Date=models.DateField()
    Accept_decline=models.IntegerField(null=True, blank=True)
    submit=models.BooleanField(default=False)
    submit_date=models.DateField(null=True, blank=True)
    submitMessage=models.TextField(null=True, blank=True)
