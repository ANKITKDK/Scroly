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


def user_type(request):
    user=request.user
    usertypeobj=UserType.objects.get(LoginType=user)
    return usertypeobj,user



# Sign-In Page  
class Signin(View):
    def get(self, request):
        return render(request, 'accounts/sign-in.html')
    
    def post(self, request):
        # if request.user.is_authenticated:
        #     return redirect('/')
        # else:
            if request.method=='POST':
                username=request.POST.get('username')
                password=request.POST.get('password')

                a=Login.objects.filter(username=username)
                print(a)

                if Login.objects.filter(username=username):
                    user=Login.objects.get(email=username)
                    user=authenticate(username=user.username,password=password)

                    print(user)

                    if user is not None:
                        login(request, user)
                        print('Login Successfully')
                        return redirect('/')
                    else:
                        print('yes')
                        messages.error(request, f"Wrong Credetials")
                        return redirect('/signin')
                elif Login.objects.filter(mobile_number=username):
                    user=Login.objects.get(mobile_number=username)
                    user=authenticate(username=user.usertype.user_id.username,password=password)

                    if user is not None:
                        login(request, user)
                        print('Login Successfully')
                        return redirect('/')
                    else:
                        messages.error(request, f"Wrong Credetials")
                        return redirect('/signin')
                else:
                    messages.error(request, f"Wrong Credetials")
                    return redirect('/signin')

            else:
                return render(request, 'account/sign-in.html')


# Sign-up Page
class SignUp(View):
    def get(self, request):
        return render(request, 'accounts/sign-up.html')
    
    def post(self, request):
        full_name = request.POST.get('full-name')
        phone=request.POST.get('Phone')
        email=request.POST.get('email')
        password=request.POST.get('password')
        term=request.POST.get('term')

        print(full_name, phone, email, password, term)
        
        password_pattern = re.compile("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$")
        mobile_pattern= re.compile("[6-9][0-9]{9}")
        
        if Login.objects.filter(username=email):
            messages.error(request, f"{email} is already taken.")
            return redirect('/signup')
        elif Login.objects.filter(email=email):
            messages.error(request, f"{email} is already taken.")
            return redirect('/signup')
        elif Login.objects.filter(mobile_number=phone):
            messages.error(request, f"{phone} is already taken.")
            return redirect('/signup')
        else:
            if term != None:
                if mobile_pattern.match(phone):
                    if len(password)>8 and re.search(password_pattern,password):
                        userobj=Login.objects.create_user(first_name=full_name,password=password,email=email,username=email,mobile_number=phone)
                        UserType.objects.create(LoginType=userobj,LoginTypeName='user')
                        user_obj=authenticate(username=email,password=password)
                        if user_obj is not None:
                            login(request, user_obj)
                            return redirect('/')
                        else:
                            return redirect('/signup')
                    else:
                        messages.error(request, f"Password length must be more than 8 character long and must contatin atleat one number,one uppercare,one lowercase and one special symbol ")
                        return redirect('/signup')
                else:
                    messages.error(request, f"Mobile is incorrect please enter you valid mobile number")
                    return redirect('/signup')
            else:
                print("Please Select terms and condition")
                return redirect('/signup')


# Logout
class Logout(View):
    @method_decorator(login_required)
    def get(self, request):
        logout(request)
        return redirect('/')


# Forgot Password page
class ForgotPassword(View):
    def get(self, request):
        return render(request, 'accounts/forgot-password.html')

# OTP Page
class OTP(View):
    def get(self, request):
        return render(request, 'accounts/otp-screen.html')

# Profile Page
class Profile(View): 
    @method_decorator(login_required(login_url='/signin'))
    def get(self, request):
        usertypeobj,userobj=user_type(request)
        catlevel1,catlevel2,catlevel3=category()
      
        try:
            profileobj=LoginProfile.objects.get(UserTypeId=usertypeobj)
        except:
            profileobj=None
        context={'user':userobj,'profileobj':profileobj, 'cat1':catlevel1,'cat2':catlevel2,'cat3':catlevel3}
        return render(request, 'accounts/profile.html',context)

    @method_decorator(login_required(login_url='/signin'))
    def post(self, request):
        alternatenumber=request.POST.get('alternate')
        gender=request.POST.get('gender')
        dob=request.POST.get('dateofbirth')
        paddress=request.POST.get('permanent-address')
        usertypeobj,userobj=user_type(request)

        if LoginProfile.objects.filter(UserTypeId=usertypeobj.id):
            LoginProfileobj=LoginProfile.objects.get(UserTypeId=usertypeobj.id)
            LoginProfileobj.AlternateMobile=alternatenumber
            LoginProfileobj.Gender=gender
            LoginProfileobj.DateOfBirth=dob
            LoginProfileobj.adderess=paddress
            LoginProfileobj.save()
        else:
            LoginProfile.objects.create(
                UserTypeId=usertypeobj,
                AlternateMobile=alternatenumber,
                Gender=gender,
                DateOfBirth=dob,
                adderess=paddress,
                )
        return redirect('/profile')


# Shilpa changes

class EditProfile(View):
    @method_decorator(login_required)
    def post(self,request):
        alternatenumber=request.POST.get('alternatenumber') 
        gender=request.POST.get('gender')
        dob=request.POST.get('dateofbirth')
        paddress=request.POST.get('permanent-address')
        usertypeobj,userobj=user_type(request)

        if LoginProfile.objects.filter(UserTypeId=usertypeobj):
            profileobj=LoginProfile.objects.get(UserTypeId=usertypeobj)
        else:
            profileobj=None
       
        mobile_pattern= re.compile("[6-9][0-9]{9}")


        print(gender)
        if profileobj!= None:
             if alternatenumber!=None:
                if mobile_pattern.match(alternatenumber):
                    profileobj.AlternateMobile=alternatenumber
                else:
                    messages.error(request, f"Phone number should start with 9,8,7,6!")
    
             if gender!=None:
                profileobj.Gender=gender
            
             if dob!=None:
                profileobj.DateOfBirth=dob
    
             if paddress!=None:
                profileobj.adderess=paddress
            
             profileobj.save()
             messages.success(request, f"Profile Updated Successfully!")
             return redirect('/profile') 

            
        else:
            messages.error(request, f"Profile Not Found!")
            return redirect('/profile') 


# Profile upload

class ProfileUpload(View):
    @method_decorator(login_required)
    def post(self,request):
        profilephoto=request.FILES['profileimage']
        usertypeobj,userobj=user_type(request)

        print(usertypeobj.id)

        if LoginProfile.objects.filter(UserTypeId=usertypeobj.id):
            profileobj=LoginProfile.objects.get(UserTypeId=usertypeobj)
            print(profileobj.ProfilePic)
            profileobj.ProfilePic=profilephoto
            profileobj.save()
            messages.success(request, f"Profile Updated Successfully!")
            return redirect('/profile')
        else:
            LoginProfile.objects.create(ProfilePic=profilephoto,UserTypeId=usertypeobj)
            return redirect('/profile')


#sawan
# class ForgotPassword(View):
#     def get(self,request):
#         return render(request,'forgot-password.html')
