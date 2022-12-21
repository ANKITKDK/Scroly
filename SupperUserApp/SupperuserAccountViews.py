
from dataclasses import is_dataclass
from multiprocessing import context
from django.shortcuts import render,redirect
from django.views import View
from django.views.generic import TemplateView
from django.contrib import messages

# from Scrolly.Accounts.views import user_type
from .models import *
import re
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from Core.views import category
from Accounts.models import * 


class SupperUserDashboard(View):
    def get(self, request):
        return render (request, "SupperUserAccounts/supperuser-dashboard.html") 

class AdminList(View):
    def get(self, request):
       
        AdminListobj=LoginProfile.objects.all()
        print('AdminListobj',AdminListobj)
        context={'AdminListobj':AdminListobj}
        return render (request, "SupperUserAccounts/admin-list.html",context)    

    def post(self, request):
        try:
            coverImage=request.FILES['coverImage']
        except:
            coverImage=None 
        
        firstname=request.POST.get("firstname")
        lastname=request.POST.get("lastname")
        username=request.POST.get("username")
        password=request.POST.get("password")
        email=request.POST.get("email")
        birthday=request.POST.get("birthday")
        address=request.POST.get("address")
        phonenumber=request.POST.get("phonenumber")
        print(username)

        # if UserType.objects.filter(LoginTypeName=username):       # for define unique slug
        #     messages.error(request, f"This username is already in use.")
        if Login.objects.filter(username=username):
            messages.error(request, f"This username is already in use.")
        elif Login.objects.filter(email=email):
            messages.error(request, f"This email is already in use.")
        elif Login.objects.filter(mobile_number=phonenumber):
            messages.error(request, f"This Phone Number is already in use.")
        else:
            newuser=Login.objects.create_user(first_name=firstname, last_name=lastname, email=email, username=username, password=password ,mobile_number=phonenumber,is_staff=True)
            obj=UserType.objects.create(LoginType=newuser, LoginTypeName='admin')
            LoginProfile.objects.create(UserTypeId=obj, ProfilePic=coverImage, DateOfBirth=birthday, adderess= address)
        return redirect("/AdminList")


class Block_AdminUser(View):
    def get(self, request, id):
        user=Login.objects.get(id=id)
        user.is_active=0
        user.save()
        messages.error(request, "User details has been Blocked")
        return redirect(f"/AdminList")   


class Unblock_AdminUser(View):
    def get(self, request, id):
        user=Login.objects.get(id=id)
        user.is_active=1
        user.save()
        messages.error(request, "User details has been unBlocked")
        return redirect(f"/AdminList")   

class UpdateAdminList(View):
    method_decorator(login_required(login_url='/AdminSignIn'))
    def get(self, request):
        return render (request, "SupperUserAccounts/admin-list.html") 

    def post(self, request, id):
        updateadminlistobj=LoginProfile.objects.get(id=id)
        print('profileid',updateadminlistobj)
        print('username : ',updateadminlistobj.UserTypeId.LoginType.username)
        try:
           updateadminlistobj.ProfilePic=request.FILES["addphoto"]  
        except:
            pass   
        
        updateadminlistobj.adderess=request.POST.get("address") 
        updateadminlistobj.UserTypeId.LoginType.first_name=request.POST.get("firstname")
        updateadminlistobj.UserTypeId.LoginType.last_name=request.POST.get("lastname")
        updateadminlistobj.UserTypeId.LoginType.username=request.POST.get("userName")
        updateadminlistobj.UserTypeId.LoginType.email=request.POST.get("email")
        updateadminlistobj.UserTypeId.LoginType.mobile_number=request.POST.get("number")
        updateadminlistobj.DateOfBirth=request.POST.get("dateofbirth")
        updateadminlistobj.save()
        updateadminlistobj.UserTypeId.LoginType.save()
        return redirect('/AdminList')  



class AdminListDetails(View):
    def get(self, request):
        usertypeobj=LoginProfile.objects.all()           #for usertype field      
        context={'usertypeobj':usertypeobj}
        return render (request, "SupperUserAccounts/admin-list-details.html",context)           