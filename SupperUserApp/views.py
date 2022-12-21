from django.shortcuts import render,redirect
from django.views import View
from django.views.generic import TemplateView
from django.contrib import messages
from .models import *
import re
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from Core.views import category


# Create your views here.
class Base(View):
    def get(self, request):
        return render (request, "SupperUserApp/superuser-base.html")

class Index(View):
    def get(self, request):
        return render (request, "SupperUserApp/index.html")



class SubCategory(View):
    def get(self, request):
        return render (request, "SupperUserApp/sub-category.html")        



class OrderHistory(View):
    def get(self, request):
        return render (request, "SupperUserApp/order-history.html") 


class ReviewList(View):
    def get(self, request):
        return render (request, "SupperUserApp/review-list.html")       

   

 

# class UserProfile(View):
#     def get(self, request):
#         return render (request, "SupperUserApp/user-profile.html")             

class VendorCard(View):
    def get(self, request):
        return render (request, "SupperUserApp/vendor-card.html")             
      
class VendorList(View):
    def get(self, request):
        return render (request, "SupperUserApp/vendor-list.html")       

class Vendorprofile(View):
    def get(self, request):
        return render (request, "SupperUserApp/vendor-profile.html")       

class BrandList(View):
    def get(self, request):
        return render (request, "SupperUserApp/brand-list.html")  

class Invoice(View):
    def get(self, request):
        return render (request, "SupperUserApp/invoice.html")                  
            

    