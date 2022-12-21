from ast import Pass
from itertools import product
from multiprocessing import context
from urllib import request
from django.shortcuts import render,redirect
from django.views import View
from django.views.generic import TemplateView
from django.contrib import messages
from Core.models import *
from django.contrib import messages
from django.db.models import Avg, Max, Min, Sum
from django.core.paginator import Paginator


from .models import *
import re
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from Core.views import category
from datetime import date
from django.db.models import Sum
from Accounts.models import * 
from datetime import datetime, date, timedelta

# Create your views here.

# Admin Sign-In class 
class AdminSignIn(View):
    def get(self, request):
        return render (request, "AdminAccount/admin-sign-in.html")

    def post(self, request):
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username , password=password)
        print(password,username)
        if user is not None:
            if user.is_staff or user.is_supperuser:
                login(request, user)
                return redirect('AdminDashboard')
            else:
                    logout(request)
                    return redirect('/AdminSignIn')    
        else:
                messages.info(request, 'Invalid Credential')   
                return redirect('/AdminSignIn')        

# Admin Logout class
class LogoutAdmin(View):
    @method_decorator(login_required(login_url='/AdminSignIn'))
    def get(self, request):
        logout(request)
        return redirect('/AdminSignIn')

# Admin Dashboard View
class AdminDashboard(View):
    @method_decorator(login_required(login_url='/AdminSignIn'))
    def get(self, request):
        return render (request, "AdminAccount/admin-dashboard.html")           

# Admin Add & view Category-1
class Category1(View):
    @method_decorator(login_required(login_url='/AdminSignIn'))
    def get(self, request):
        categorylevel1=CategoryLevel1.objects.all()
        paginator = Paginator(categorylevel1,10)
        page_number=request.GET.get('page')
        print(page_number)
        page_obj = paginator.get_page(page_number)
        print(page_obj)
        categorylevel2obj=CategoryLevel2.objects.all()
        categorylevel2obj1=CategoryLevel2.objects.all().count()
        print('category',categorylevel2obj)
        context={'categorylevel1':page_obj, 'categorylevel2obj':categorylevel2obj, 'categorylevel2obj1':categorylevel2obj1}
        return render (request, "AdminAccount/category-1.html",context)   

    @method_decorator(login_required(login_url='/AdminSignIn'))
    def post(self, request):
        name=request.POST.get('name')
        slug=request.POST.get('slug')
        fulldescription=request.POST.get('fulldescription')
        try:
            addphoto=request.FILES['addphoto']
        except:
            addphoto=None

        if CategoryLevel1.objects.filter(CategorySlug=slug):
         messages.error(request, f"This Slug is already in use.")
        else:

            if bool(re.search(r"\s", slug)):                  #for avoiding slug space error 
               print("yes")
               messages.error(request,'Not Valid slug')
            else:    
                    CategoryLevel1.objects.create(
                                            CategoryName=name,
                                            CategoryImage=addphoto,
                                            CategoryDescription=fulldescription,
                                            CategorySlug=slug)
                    messages.error(request, f"Category Added Successfully.")
            return redirect ("/Category1") 

# Edit Category-1
class UpdateCategory1(View):
    method_decorator(login_required(login_url='/AdminSignIn'))
    def get(self, request):
        return render (request, "AdminAccount/category-1.html") 

    def post(self, request, id):
        updatecategory1obj=CategoryLevel1.objects.get(id=id)
        print(request.POST  )
        updatecategory1obj.CategoryName=request.POST.get("name")
        print('chevk',updatecategory1obj.CategoryName)
        updatecategory1obj.CategoryDescription=request.POST.get("fulldescription")
        try:
           updatecategory1obj.CategoryImage=request.FILES["addphoto"]
        except:
            pass 
        updatecategory1obj.save()
        return redirect('/Category1')

# Delete Category-1
class DeleteCategory1(View):
    method_decorator(login_required(login_url='/AdminSignIn'))
    def get(self, request, id):
        delete_category_1=CategoryLevel1.objects.get(id=id)
        delete_category_1.delete()
        return redirect (f"/Category1")

# Add & View Category-2
class Category2(View):
    method_decorator(login_required(login_url='/AdminSignIn'))
    def get(self, request):
        categorylevel1=CategoryLevel1.objects.all()
        categorylevel2=CategoryLevel2.objects.all()
        categorylevel3obj=CategoryLevel3.objects.all()
        categorylevel3obj1=CategoryLevel3.objects.all().count()
        context={'categorylevel2':categorylevel2,'categorylevel1':categorylevel1, 'categorylevel3obj':categorylevel3obj, 'categorylevel3obj1':categorylevel3obj1}
        return render (request, "AdminAccount/category-2.html",context) 

    @method_decorator(login_required(login_url='/AdminSignIn'))
    def post(self, request):
        name=request.POST.get("name")
        slug=request.POST.get("slug")
        categorylevel1=request.POST.get("categorylevel1")
        categorylevel1obj=CategoryLevel1.objects.get(id=categorylevel1)
        fulldescription=request.POST.get("fulldescription")
        try:  
            addphoto=request.FILES["addphoto"]
        except:
            addphoto=None    
        
        if CategoryLevel2.objects.filter(CategorySlug=slug):
             messages.error(request, f"This Slug is already in use.")

        else:   
             if bool(re.search(r"\s", slug)):                        #for avoiding slug space error 
               print("yes")
               messages.error(request,'Not Valid slug')
             else:                              
                 CategoryLevel2.objects.create(CategoryLevel2Name=name,
                                                CategoryLevel1Id=categorylevel1obj,
                                                CategoryImages=addphoto,
                                                CategoryDescription=fulldescription,
                                                CategorySlug=slug)                 
                 messages.error(request, f"Category Added Successfully.")                            
        return redirect ("/Category2")  

# Edit Category-2
class UpdateCategory2(View):
    method_decorator(login_required(login_url='/AdminSignIn'))
    def get(self, request):
        return render (request, "AdminAccount/category-2.html") 

    def post(self, request, id):
        updatecategory2obj=CategoryLevel2.objects.get(id=id)
        print(request.POST  )
        updatecategory2obj.CategoryLevel2Name=request.POST.get("name")     #use model field
        updatecategory2obj.CategoryDescription=request.POST.get("fulldescription")
        try:
            updatecategory2obj.CategoryImages=request.FILES["addphoto"]
        except:
            pass
        updatecategory2obj.save()
        return redirect('/Category2')    
    
# Delete Category-2
class DeleteCategory2(View):
    method_decorator(login_required(login_url='/AdminSignIn'))
    def get(self, request, id):
        delete_category_2=CategoryLevel2.objects.get(id=id)
        delete_category_2.delete()
        return redirect (f"/Category2")

# Add & View Category-3
class Category3(View):
    @method_decorator(login_required(login_url='/AdmiSignIn'))
    def get(self, request):
        categorylevel2=CategoryLevel2.objects.all()
        categorylevel3=CategoryLevel3.objects.all()
        context={'categorylevel3':categorylevel3,'categorylevel2':categorylevel2 }
        return render (request, "AdminAccount/category-3.html",context) 

    @method_decorator(login_required(login_url='/AdmiSignIn'))
    def post(self, request):
        name=request.POST.get("name")
        slug=request.POST.get("slug")
        categorylevel2=request.POST.get("categorylevel2")
        categorylevel2obj=CategoryLevel2.objects.get(id=categorylevel2)
        fulldescription=request.POST.get("fulldescription")
        try:
            addphoto=request.FILES["addphoto"]
        except:
            addphoto=None

        # print(addphoto)
        if CategoryLevel3.objects.filter(CategorySlug=slug):       # for define unique slug
            messages.error(request, f"This Slug is already in use.")

        else:   

             if bool(re.search(r"\s", slug)):                             #for avoiding slug space error 
               print("yes")
               messages.error(request,'Not Valid slug')
             else: 
                 CategoryLevel3.objects.create(CategoryLevel3Name=name,CategoryLevel2Id=categorylevel2obj,
                                                    CategoryDescription=fulldescription,
                                                    CategoryImages=addphoto,
                                                    CategorySlug=slug)  
                 messages.error(request,f"Category Added Successfully.")
             return redirect ("/Category3")  

# Edit Category-3
class UpdateCategory3(View):
    method_decorator(login_required(login_url='/AdminSignIn'))
    def get(self, request):
        return render (request, "AdminAccount/category-3.html") 

    def post(self, request, id):
        updatecategory3obj=CategoryLevel3.objects.get(id=id)
        print(request.POST  )
        updatecategory3obj.CategoryLevel3Name=request.POST.get("name")     #use model field
        updatecategory3obj.CategoryDescription=request.POST.get("fulldescription")
        try:
            updatecategory3obj.CategoryImages=request.FILES["addphoto"]
        except:
            pass
        updatecategory3obj.save()
        return redirect('/Category3')

# Delete Category-3
class DeleteCategory3(View):
    method_decorator(login_required(login_url='/AdminSignIn'))
    def get(self, request, id):
        delete_category_3=CategoryLevel3.objects.get(id=id)
        delete_category_3.delete()
        return redirect (f"/Category3")

# Add Product
class AddProduct(View):
    def get(self, request):
        catlevel1,catlevel2,catlevel3=category()
        ProductColorobj=ProductColor.objects.all()
        ProductSizeobj=ProductSize.objects.all()
        context={'cat1':catlevel1,'cat2':catlevel2,'cat3':catlevel3,"ProductColorobj":ProductColorobj, "ProductSizeobj":ProductSizeobj}
        return render (request, "AdminAccount/product-add.html",context) 

    def post(self, request):
        if request.method == 'POST':
            mainimage=request.FILES['mainimage']
            try:
                file1=request.FILES['file1']
            except:
                file1=None
            try:
                file2=request.FILES['file2']
            except:
                file2=None
            try:
                file3=request.FILES['file3']
            except:
                file3=None
            try:
                file4=request.FILES['file4']
            except:
                file4=None
            try:
                file5=request.FILES['file5']
            except:
                file5=None
            try:
                file6=request.FILES['file6']
            except:
                file6=None
            productname=request.POST.get('Productname')
            Brandname= request.POST.get('Brandname')
            

            selectcategories=request.POST.get('selectcategories')
            category3obj=CategoryLevel3.objects.get(id=selectcategories)
            slug=request.POST.get('slug') 
            fulldetail=request.POST['fulldetail']
            


            productcount=Product.objects.filter(CategoryLevel3Id=category3obj).count()   # product count in category3

            if Product.objects.filter(ProductSlug=slug):
                print('Slug Already Taken!')
                messages.error(request,'Slug Already Taken!')
            else:
                if bool(re.search(r"\s", slug)):
                    print('Not Valid slug')
                    messages.error(request,'Not Valid slug')
                else:
                    Product.objects.create(
                                    CategoryLevel1Id=category3obj.CategoryLevel2Id.CategoryLevel1Id,
                                    CategoryLevel2Id=category3obj.CategoryLevel2Id,
                                    CategoryLevel3Id=category3obj,
                                    ProductName=productname,
                                   ProductDescription=fulldetail,
                                   ProductSlug=slug,
                                   ProductMainImage=mainimage,
                                   ProductBrandName=Brandname,
                                   file1=file1,file2=file2,file3=file3,file4=file4,file5=file5,file6=file6)
                category3obj.productcount=productcount+1
                print('yes')
            category3obj.save()
            return redirect('/AddProduct')

# view product list
class ProductList(View):
    def get(self, request):
        AddProductobj=Product.objects.all()
        paginator = Paginator(AddProductobj,10)
        page_number=request.GET.get('page')
        print(page_number)
        page_obj = paginator.get_page(page_number)
        print(page_obj)
        context={'AddProductobj':page_obj}
        return render (request, "AdminAccount/product-list.html", context)  

# edit product list
class UpdateProductList(View):
    method_decorator(login_required(login_url='/AdminSignIn'))
    def get(self, request):
        return render (request, "AdminAccount/product-list.html") 

    def post(self, request, id=None, slug=None):
        if slug!=None:
            Upadete_description=Product.objects.get(ProductSlug=slug)
            Upadete_description.ProductName=request.POST.get("name")
            Upadete_description.ProductBrandName=request.POST.get("brandname")
            try:
                Upadete_description.ProductDescription=request.POST.get("description")
            except:
                pass
            Upadete_description.save()
            return redirect(f"/ProductDetailAdmins/{slug}")
        else:
            updateproductlistobj=Product.objects.get(id=id)
            # print(request.POST  )
            updateproductlistobj.ProductName=request.POST.get("name")     #use model field
            updateproductlistobj.ProductBrandName=request.POST.get("brandname")     #use model field
            # updateproductlistobj.ProductMainImage=request.FILES["addphoto"]
            updateproductlistobj.save()
            return redirect('/ProductList') 

# Delete product from list    
class DeleteProductList(View):
    method_decorator(login_required(login_url='/AdminSignIn'))
    def get(self, request, id):
        Product_obj=Product.objects.get(id=id)
        Product_obj.delete()
        return redirect (f"/ProductList")


class ProductManage(View):
    def get(self, request):
        return render (request, "AdminAccount/product-manage.html")   

# Add & View Product Color
class AddColor(View):
    def get(self, request):
        ProductColorobj=ProductColor.objects.all()
        print(ProductColorobj)
        context={"ProductColorobj":ProductColorobj}
        return render(request,'AdminAccount/Colour.html',context)   

    def post(self, request):
        addcolor=request.POST.get("addcolor")
        if ProductColor.objects.filter(ProductColorName=addcolor):
            print('That Color is already avaliable')
        else:
            ProductColor.objects.create(ProductColorName=addcolor)
        return redirect('/AddColor')

# Update Product Color
class UpdateColor(View):
    def get(self, request):
        ProductColorobj=ProductColor.objects.all()
        context={"ProductColorobj":ProductColorobj}
        return render(request,'AdminAccount/Colour.html',context)
    
    def post(self, request, id):
        color_obj=ProductColor.objects.get(id=id)
        color_obj.ProductColorName=request.POST.get("color")
        color_obj.save()
        return redirect('/AddColor')

# Delete Product Color
class DeleteColor(View):
    def get(self, request, id):
        color_obj=ProductColor.objects.get(id=id)
        color_obj.delete()
        return redirect('/AddColor')

# Add & View Product Color Image from admin
class AddProductColourImage(View):
    def get(self, request):
        ProductColourobj=ProductColor.objects.all()
        ProductColourImageobj=ProductColourImage.objects.all()
        return render(request,'AdminAccount/AddProductColourImage.html',{'ProductColourobj':ProductColourobj,'ProductColourImageobj':ProductColourImageobj})   

    def post(self, request):
        imagename=request.POST.get("imagename")
        selectcolour=request.POST.get("selectcolour")
        colourobj=ProductColor.objects.get(id=selectcolour)
        try:
            addphoto=request.FILES['addphoto']
        except:
            pass    
        
        if ProductColourImage.objects.filter(ProductImageName=imagename):
            print("That Image name is already exits")
        else:
            ProductColourImage.objects.create(ProductImageName=imagename,ProductColor=colourobj,
                                        ProductColourImage=addphoto
                            )
        return redirect('/AddProductColourImage')

# Update Product Color Image from admin
class UpdateProductColourImage(View):
    method_decorator(login_required(login_url='/AdminSignIn'))
    def get(self, request):
       
        return render(request,'AdminAccount/AddProductColourImage.html',context)
    
    def post(self, request, id):
        productcolorimg_obj=ProductColourImage.objects.get(id=id)
        productcolorimg_obj.ProductImageName=request.POST.get("imagename")
        try:
           productcolorimg_obj.ProductColourImage=request.FILES["addimage"]
        except:
              pass

        productcolorimg_obj.save()
        
        return redirect('/AddProductColourImage')

#Delete Product Color Image from admin
class DeleteProductColourImage(View):
    def get(self, request,id):
        productcolorimg_obj=ProductColourImage.objects.get(id=id)
        productcolorimg_obj.delete()
        return redirect('/AddProductColourImage')

 # Add & View Product Size 
class AddSize(View):
    def get(self, request): 
        ProductSizeobj=ProductSize.objects.all()
        context={'ProductSizeobj':ProductSizeobj}
        return render(request, "AdminAccount/Size.html",context)   

    def post(self, request):
        addsize=request.POST.get("addsize")
        if ProductSize.objects.filter(size=addsize):
            print("That Size is already exits")
        else:
            ProductSize.objects.create(size=addsize)
        return redirect("/AddSize")

# Update Product Size from admin
class UpdateSize(View):
    def get(self, request):
        ProductSizeobj=ProductSize.objects.all()
        context={'ProductSizeobj':ProductSizeobj}
        return render(request, "AdminAccount/Size.html",context)
    
    def post(self, request, id):
        size_obj=ProductSize.objects.get(id=id)
        size_obj.size=request.POST.get("size")
        size_obj.save()
        return redirect("/AddSize")

# Delete Product Size from admin
class DeleteSize(View):
    def get(self, request, id):
        size_obj=ProductSize.objects.get(id=id)
        size_obj.delete()
        return redirect("/AddSize")


# Add & View Product color, Size & question answer in Product Detail page
from django.db.models import Min
class ProductDetail(View):
    def get(self,request,slug):
        productobj=Product.objects.get(ProductSlug=slug)
        allproduct=ProductSizeColor.objects.filter(Product=productobj)
        allquestionandanswer=QuestionsAndAnswers.objects.filter(ProductId=productobj)
        ProductColorobj=ProductColor.objects.all()
        ProductSizeobj=ProductSize.objects.all()
        ProductColourImageobj=ProductColourImage.objects.all()
        print(ProductColorobj)

        context={'ProductColourImageobj':ProductColourImageobj,'ProductSizeobj':ProductSizeobj,'ProductColorobj':ProductColorobj,'productobj':productobj ,'allproduct':allproduct ,'allquestionandanswer':allquestionandanswer}
        return render (request, "AdminAccount/product-detail.html", context)       

    def post(self, request, slug):
        productobj=Product.objects.get(ProductSlug=slug)
        total=ProductSizeColor.objects.filter(Product=productobj).aggregate(total=Sum('Stock'))
        selectcolour=request.POST["selectcolour"]
        entersize=request.POST["entersize"]
        image=request.FILES["image"]
        prize=request.POST.get('prize')
        Discount=request.POST.get('Discount')
        enterstock=request.POST.get("enterstock")

        try:
            productobj.TotalProduct=int(total['total'])+int(enterstock)
        except:
            productobj.TotalProduct=int(enterstock)

        productobj.save()

        colourobj=ProductColor.objects.get(id=selectcolour)
        sizeobj=ProductSize.objects.get(id=entersize)

        if ProductSizeColor.objects.filter(Product=productobj).filter(ProductSize=sizeobj).filter(ProductColour=colourobj):
            print("Product Of Same size And Colour is allready available")
        else:
            ProductSizeColor.objects.create(Product=productobj,ProductColour=colourobj,ProductSize=sizeobj,ProductImage=image,Stock=enterstock,Price=prize,DiscountPercent=Discount)

        minimumprize=ProductSizeColor.objects.filter(Product=productobj).values('Price').aggregate(Min('Price'))['Price__min']
        minimumproductprizeobj=ProductSizeColor.objects.filter(Product=productobj).filter(Price=minimumprize).last()

        productobj.Price=minimumproductprizeobj.Price
        productobj.DiscountPercent=minimumproductprizeobj.DiscountPercent
        productobj.save()

        return redirect(f'/ProductDetailAdmins/{slug}')  

# Edit Product Image
class UpdateProductImage(View):
    method_decorator(login_required(login_url='/AdminSignIn'))
    def get(self, request):
        return render (request, "AdminAccount/product-detail.html") 
    def post(self, request, slug):
        updateproductimgobj=Product.objects.get(ProductSlug=slug)

        # main Inage
        try:
            updateproductimgobj.ProductMainImage=request.FILES['mainimage']
        except:
            pass

        # image 1
        try:
            updateproductimgobj.file1=request.FILES['file1']
        except:
            pass
        
        # image 2
        try:
            updateproductimgobj.file2=request.FILES['file2']
        except:
            pass

        # image 3
        try:
            updateproductimgobj.file3=request.FILES['file3']
        except:
            pass

        # image 4
        try:
            updateproductimgobj.file4=request.FILES['file4']
        except:
            pass

        # image 5
        try:
            updateproductimgobj.file5=request.FILES['file5']
        except:
            pass

        # image 6
        try:
            updateproductimgobj.file6=request.FILES['file6']
        except:
            pass
        updateproductimgobj.save()
        return redirect(f'/ProductDetailAdmins/{slug}')

# Edit Product Details (Size, Color, Stock, Discount, Prize)
class UpdateProductDetails(View):

    method_decorator(login_required(login_url='/AdminSignIn'))
    def get(self, request):
        return render (request, "AdminAccount/product-detail.html") 

    def post(self, request, id):
        updateproductdetailstobj=ProductSizeColor.objects.get(id=id)

        try:
            image=request.FILES['image']
            updateproductdetailstobj.ProductImage=image
        except:
            pass
        updateproductdetailstobj.ProductSize=ProductSize.objects.get(id=request.POST.get('entersize'))
        updateproductdetailstobj.ProductColour=ProductColor.objects.get(id=request.POST.get('selectcolour'))
        updateproductdetailstobj.Price=request.POST.get("prize")
        updateproductdetailstobj.DiscountPercent=request.POST.get("Discount")
        updateproductdetailstobj.Stock=request.POST.get("enterstock")     #use model field
       
        updateproductdetailstobj.save()
        return redirect(f'/ProductDetailAdmins/{updateproductdetailstobj.Product.ProductSlug}')    # "{}" bracket logic add to solve page not found error its conflict between slug & id in url      

# Delete Product Details (Size, Color, Stock, Discount, Prize)
class DeleteProductDetails(View):
    def get(self, request, id):
        productDetails_id=ProductSizeColor.objects.get(id=id)
        productDetails_id.delete()
        return redirect(f'/ProductDetailAdmins/{productDetails_id.Product.ProductSlug}')

# View All Products
class ProductGride(View):
    def get(self, request):
       productgride=Product.objects.all()
       
    #    productgrideprize=ProductSizeColor.objects.filter(Product=productgride)


    #    print(productgrideprize)
       context={'productgride':productgride,}
       return render (request, "AdminAccount/product-grid.html",context) 


# add Ckeditor on product detail page
class Product_Details(View):
    def post(self, request, id):
        product_obj=Product.objects.get(id=id)
        print(id)
        product_obj.Product_Specification=request.POST['editor1']
        product_obj.save()
        return redirect(f"/ProductDetailAdmins/{product_obj.ProductSlug}")

# Add & View Question & Answer in Product Detail page
class Questionandanswer(View):
    def get(self, request):
        questionanswerobj=QuestionsAndAnswers.objects.all()
        context={"questionanswerobj":questionanswerobj}
        return render (request, "SupperUserApp/product-detail.html", context)

    def post(self, request, slug):
        # print("anushree")
        productobj=Product.objects.get(ProductSlug=slug)
        addquestions=request.POST.get("addquestions")
        addanswers=request.POST.get("addanswers")
        user=request.user
        
        print(" anushree",addquestions)

        QuestionsAndAnswers.objects.create(ProductId=productobj,Question=addquestions,Answer=addanswers,Addedby=user)
        return redirect(f"/ProductDetailAdmins/{slug}")

#Edit Question & Answer in Product Detail page
class UpdateQuestionAndAnswer(View):
    method_decorator(login_required(login_url='/AdminSignIn'))
    def get(self, request):
        return render (request, "AdminAccount/product-list.html") 

    def post(self, request, id):
        updatequeandansobj=QuestionsAndAnswers.objects.get(id=id)
        # print(request.POST  )
        updatequeandansobj.Question=request.POST.get("question")               #use model field
        updatequeandansobj.Answer=request.POST.get("answer")                 #use model field
 
        updatequeandansobj.save()
        return redirect(f'/ProductDetailAdmins/{updatequeandansobj.ProductId.ProductSlug}')   

#Delete Question & Answer in Product Detail page
class DeleteQuestionAndAnswer(View):
    method_decorator(login_required(login_url='/AdminSignIn'))
    def get(self, request, id):
        Question=QuestionsAndAnswers.objects.get(id=id)
        Question.delete()
        return redirect(f'/ProductDetailAdmins/{Question.ProductId.ProductSlug}')

# Show Normal User list in Admin
class NoramlUserList(View):
    def get(self, request):
        NormalUserListobj=UserType.objects.filter(LoginTypeName='user')
        # NormalUserListobj = LoginProfile.objects.all()
        print("NormalUserListobj",NormalUserListobj)
        context={'NormalUserListobj':NormalUserListobj }
        return render (request, "AdminAccount/normal-user-list.html",context)         

# Block Normal User from list
class Block_NormalUser(View):
    def get(self, request, id):
        user=Login.objects.get(id=id)
        user.is_active=0
        user.save()
        messages.error(request, "User details has been Blocked")
        return redirect(f"/NoramlUserList")   

# UnBlock Normal User from list
class Unblock_NormalUser(View):
    def get(self, request, id):
        user=Login.objects.get(id=id)
        user.is_active=1
        user.save()
        messages.error(request, "User details has been unBlocked")
        return redirect(f"/NoramlUserList")   


#  View Normal User Profile & Update its Password & show add to cart product 
class NormalUserProfile(View):
    def get(self, request, id):
        usertypeobj=UserType.objects.get(id=id)      #for usertype field
        print("usertypeobj",usertypeobj)
        if LoginProfile.objects.filter(UserTypeId=usertypeobj):    #for loginprofile field
            login_obj=LoginProfile.objects.get(UserTypeId=usertypeobj)
            print('login_obj',login_obj)
            login_obj.ProfilePic
            
        else:
            login_obj=None
        
        addtocartobj=AddToCart.objects.filter(LoginId=usertypeobj.LoginType)   #show add to cart product in normal user profile
        print(addtocartobj)
        context={'usertypeobj':usertypeobj, 'login_obj':login_obj , 'addtocartobj':addtocartobj}
        
        return render (request, "AdminAccount/normal-user-profile.html",context)             
    
    def post(self, request,id):
        setobj=UserType.objects.get(id=id)
        userobj=setobj.LoginType
        
        newpassword=request.POST.get("newpassword")
        confnewPassword=request.POST.get("confnewpassword")
        if newpassword==confnewPassword:
            userobj.set_password('newpassword')
            userobj.save()
        
        return redirect(f'/NormalUserProfile/{setobj.LoginType.id}')   




# class AddProductColour(View):
#     def get(self, request):
#         return render(request,'AdminAccount/Colour.html')

# class AddProductSize(View):
#     def get(self, request):
#         return render(request,'AdminAccount/Size.html')

# class AddProductColour(View):
#     def get(self, request):
#         return render(request,'AdminAccount/Image.html'


# Add & view Home categories Title for scrolly home page
class HomeCategoryView(View):
    def get(self, request, id=None):
        if id==None:
            HomeCategoryobj=HomeCategory.objects.all()
            context={'HomeCategoryobj':HomeCategoryobj }
            return render(request, "AdminAccount/homecategory.html",context)
        else:
            HomeCategoryobj=HomeCategory.objects.get(id=id)
            HomeCategoryobj.delete()
            return redirect('/HomeCategory')

    def post(self, request, id=None):

        if id==None:
            name=request.POST.get("name")
            slugname=request.POST.get("slug")
            if HomeCategory.objects.filter(HomeCategorySlug=slugname):
                print("This Slug is Already taken")
            else:
                HomeCategory.objects.create(HomeCategoryName=name,HomeCategorySlug=slugname )
            return redirect('/HomeCategory')
        elif id!=None:

            HomeCategoryobj=HomeCategory.objects.get(id=id)
            name=request.POST.get("name")
            # slugname=request.POST.get("slug")

            HomeCategoryobj.HomeCategoryName=name
            # HomeCategoryobj.HomeCategorySlug=slugname

            HomeCategoryobj.save()
            return redirect('/HomeCategory')


#anushree code
# Add & view Home categories Product Name for scrolly home page
class HomeProduct(View):
    def get(self, request):
        homeproductnameobj=HomeCategory.objects.all()
        HomeSubCategoryobj=HomeSubCategory.objects.all()
        homeproductobj=Product.objects.all()
        context={'HomeSubCategoryobj':HomeSubCategoryobj,'homeproductnameobj':homeproductnameobj, 'homeproductobj':homeproductobj}
        return render(request, "AdminAccount/home-product.html",context)
    def post(self, request):
        home1=request.POST['home1']
        pro=request.POST['pro']
        obj1=HomeCategory.objects.get(id=home1)
        obj2=Product.objects.get(id=pro)
        print('check',home1,obj2)

        HomeSubCategory.objects.create(ProductId=obj2,HomeCategory=obj1)
        return redirect('/HomeProduct')


# Update Home Product Name for scrolly home page
class UpdateHomeProduct(View):
    def post(self, request, id):
        updatehomeproductobj=HomeSubCategory.objects.get(id=id)
        try:
            updatehomeproductobj.ProductId=Product.objects.get(id=request.POST.get("pro"))
        except:
            pass
        try:
            updatehomeproductobj.HomeCategory=HomeCategory.objects.get(id=request.POST.get("home1"))
        except:
            pass
        updatehomeproductobj.save()
        return redirect('/HomeProduct')  

# Delete Home Product Name for scrolly home page
class DeleteHomeProduct(View):
    def get(self, request, id):
        deletehomeproductobj=HomeSubCategory.objects.get(id=id)
        deletehomeproductobj.delete()
        return redirect("/HomeProduct")

# Add & views home banner images nd title
class HomeBannerView(View):
    def get(self,request):
        Homebannerlistobj=Homebannerlist.objects.all()
        return render(request, "AdminAccount/homebanner.html",{'Homebannerlistobj':Homebannerlistobj})
    
    def post(self,request):
        BannerTitle=request.POST.get('BannerTitle')
        BannerDiscount=request.POST.get('BannerDiscount')
        BannerSubtitle=request.POST.get('BannerSubtitle')
        BannerBackgroundimg=request.FILES['BannerBackgroundimg']
        Bannersideimg=request.FILES['Bannersideimg']
        Homebannerlist.objects.create(BannerTitle=BannerTitle,BannerDiscount=BannerDiscount,BannerSubtitle=BannerSubtitle,BannerBackgroundimg=BannerBackgroundimg,Bannersideimg=Bannersideimg)

        return redirect("/HomeBanner")

# Delete Home banner images nd title
class DeteleHomeBanner(View):
    def get(self, request,id):
        deletehomebannerobj=Homebannerlist.objects.get(id=id)
        deletehomebannerobj.delete()
        return redirect("/HomeBanner")


# Add & View Home Bollywood Theme name & Image for scrolly home page
class HomeBollyWood(View):
      def get(self, request):
        homeproductnameobj=HomeCategory.objects.all()
        BollyWoodCategoryObj=BollyWoodCategory.objects.all()
        context={'homeproductnameobj':homeproductnameobj, 'BollyWoodCategoryObj':BollyWoodCategoryObj,}
        return render(request, "AdminAccount/home-bollywood.html",context)
      
      def post(self, request):
        bollywoodthemeheading=request.POST.get('bollywoodthemeheading')
        print('bollywoodthemeheading',bollywoodthemeheading)
       
        bollywoodslug=request.POST.get('bollywoodslug')
        try:
            bollywoodmainimage=request.FILES['bollywoodmainimage']
        except:
                bollywoodmainimage=None
        if BollyWoodCategory.objects.filter(BollyWoodCategorySlug=bollywoodslug):
            messages.error(request, f"This Slug is already in use.")

        else:
             if bool(re.search(r"\s", bollywoodslug)):                  #for avoiding slug space error 
                print("yes")
                messages.error(request,'Not Valid slug')
             else:  
            
                  BollyWoodCategory.objects.create(TagLine=bollywoodthemeheading, MainImage=bollywoodmainimage, BollyWoodCategorySlug=bollywoodslug)
             return redirect("/HomeBollyWood")

# Delete Home Bollywood Theme name & Image for scrolly home page
class DeleteHomeBollyWood(View):
    def get(self, request, id):
        deletehomebollywoodobj=BollyWoodCategory.objects.get(id=id)
        print('deletehomebollywoodobj',deletehomebollywoodobj)
        deletehomebollywoodobj.delete()
        return redirect("/HomeBollyWood")

# Add & View Home Bollywood Product name for scrolly home page
class HomeBollyWoodProduct(View):
    def get(self, request):
        BollyWoodCategoryObj1=BollyWoodCategory.objects.last()
        homeproductobj=Product.objects.all()
        homebollywoodproductobj=BollyWoodSubCategory.objects.all()
        context={'BollyWoodCategoryObj1':BollyWoodCategoryObj1, 'homeproductobj':homeproductobj, 'homebollywoodproductobj':homebollywoodproductobj}
        return render(request, "AdminAccount/home-bollywood-product.html",context)   
            
    def post(self, request):
      
                bwtitlename=request.POST.get("bwtitlename")
                bwproductname=request.POST.get("bwproductname")
                obj2=Product.objects.get(id=bwproductname)

                BollyWoodSubCategory.objects.create(BollyWoodCategoryName=bwproductname, ProductDetails=obj2)
                return redirect('/HomeBollyWoodProduct')        
        
# Delete Home Bollywood Product name for scrolly home page
class DeleteHomeBollyWoodProduct(View):
    def get(self, request, id):
        deletehomebollywoodprdobj=BollyWoodSubCategory.objects.get(id=id)
        deletehomebollywoodprdobj.delete()
        return redirect("/HomeBollyWoodProduct")        


# View Order List for Aadmin
class NewOrder(View):
    def get(self, request):
        neworderobj=AddToCart.objects.filter(MoneyStatus=True)[::-1 ]
        context={'neworderobj':neworderobj}
        return render (request, "AdminAccount/new-order.html",context) 
    
    def post(self, request,id):
        AddToCartobj=AddToCart.objects.get(id=id)
        AddToCartobj.ProductSizeColorId.Stock=AddToCartobj.ProductSizeColorId.Stock-AddToCartobj.Qunatity
        AddToCartobj.ProductSizeColorId.save()
        AddToCartobj.DeliveryStatus=True
        AddToCartobj.DeliveryDate=datetime.today()
        return_date = datetime.today() + timedelta(days=5)
        AddToCartobj.ReturnrequestbyDate=return_date
        AddToCartobj.save()
        return redirect('/NewOrder')


# View Order List for Aadmin
class Return_Order(View):
    def get(self, request, id=None):
        # neworderobj=AddToCart.objects.filter(MoneyStatus=True)[::-1]
        if id!=None:
            print(id)
            accept=Return_Product.objects.get(id=id)
            accept.submit=True
            accept.submit_date=date.today()
            accept.ProductId.RefundStatus=1
            refund_date=datetime.today() + timedelta(days=3)
            accept.ProductId.RefundDate=refund_date
            accept.ProductId.save()
            accept.Accept_decline=1
            accept.save()
            neworderobj=Return_Product.objects.all()[::-1]
        else:
            neworderobj=Return_Product.objects.all()[::-1]
        context={'neworderobj':neworderobj}
        return render (request, "AdminAccount/return-order.html",context) 
    
    def post(self, request,id):
        decline=Return_Product.objects.get(id=id)
        print(decline)
        decline.submitMessage=request.POST.get("decription")
        decline.submit_date=date.today()
        decline.Accept_decline=1
        decline.save()
        return redirect('/Return_Order')