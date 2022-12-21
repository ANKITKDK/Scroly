from datetime import date
from urllib import request 
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
# from django.views.generic import TemplateView
# from django.contrib import messages
from SupperUserApp.models import *
from .models import *
from Accounts.models import *
import razorpay
from django.conf import settings
import random
from django.http import JsonResponse
from django.http import HttpResponseRedirect


# Create your views here.

def category():
    catlevel1=CategoryLevel1.objects.all()
    catlevel2=CategoryLevel2.objects.all()
    catlevel3=CategoryLevel3.objects.all()
    return catlevel1,catlevel2,catlevel3

# Anushree code
# It will return the current login user object, usertype object and profile object
def userprofile(request):
    if request.user.is_authenticated:
        userobj=request.user
        try:
            usertypeobj=UserType.objects.get(LoginType=userobj)
        except:
            usertypeobj=UserType.objects.create(LoginType=userobj)
        if LoginProfile.objects.filter(UserTypeId=usertypeobj):
            LoginProfileobj= LoginProfile.objects.get(UserTypeId=usertypeobj)
        else:
            LoginProfileobj= None
        return userobj, usertypeobj, LoginProfileobj
    else:
         return None,None,None
 
# shilpa code
class base1(View):
    def get(self, request):
        userobj, usertypeobj, LoginProfileobj= userprofile(request)
        catlevel1,catlevel2,catlevel3=category()
        cart_count=AddToCart.objects.filter(LoginId=userobj, MoneyStatus=0).count()
        context={'cart_count':cart_count,'cat1':catlevel1,'cat2':catlevel2,'cat3':catlevel3}
        return render(request, 'core/base1.html',context)

from django.db.models import Min, Max
class base2(View):
    def get(self, request):
        catlevel1,catlevel2,catlevel3=category()
        userobj, usertypeobj, LoginProfileobj= userprofile(request)

    
        brands=Product.objects.all()

        product=brands.values('ProductBrandName').distinct()
        print(product)
       
        Price=brands.aggregate(Min('Price'), Max('Price'))
        print(Price)
        # color_id=request.GET.get('color')
        # if color_id:
            
        #     colors=ProductColor.objects.filter(ProductColorName=color_id)
        #     print(colors)
        # else:
        #     colors=ProductColor.objects.all()

        # category2_obj=Product.objects.all()
        # category_obj=CategoryLevel2.objects.filter(CategoryLevel2Name=category2_obj)
        # print('obj',brands)
        cart_count=AddToCart.objects.filter(LoginId=userobj, MoneyStatus=0).count()
        context={'cart_count':cart_count,'cat1':catlevel1,'cat2':catlevel2,'cat3':catlevel3,'brands':product,'Price':Price}
        return render(request, 'core/base2.html',context)        
  
# Sign-In Page  
class Home(View):
    def get(self, request):
        userobj, usertypeobj, LoginProfileobj= userprofile(request)
        HomeBannerobj=Homebannerlist.objects.last()
        catlevel1,catlevel2,catlevel3=category()
        homecategoryobj1=HomeCategory.objects.all()[:2]
        homecategoryobj2=HomeCategory.objects.all()[2:]
        print('homecategoryobj2',homecategoryobj2)
        homesubcategoryobj1=HomeSubCategory.objects.all()
        print('homesubcategoryobj1',homesubcategoryobj1)
        BollyWoodobj=BollyWoodCategory.objects.last()
        string=BollyWoodobj.TagLine
        all_words = string.split()
        first_word= all_words[0]
        all_words.pop(0)
        second_word=" "
        second_word=second_word.join(all_words)

        homebollywoodproductobjrow1=BollyWoodSubCategory.objects.all()[0:10]
        homebollywoodproductobjrow2=BollyWoodSubCategory.objects.all()[10:20]

        # print('BollyWoodobj',homebollywoodproductobj)
        
        cart_count=AddToCart.objects.filter(LoginId=userobj, MoneyStatus=0).count()
        context={'cart_count':cart_count,'first_word':first_word,'second_word':second_word,'HomeBannerobj':HomeBannerobj,'cat1':catlevel1,'cat2':catlevel2,'cat3':catlevel3,'homecategoryobj2':homecategoryobj2,'homecategoryobj1':homecategoryobj1,'homecategoryobj1':homecategoryobj1,'homesubcategoryobj1':homesubcategoryobj1, 'BollyWoodobj':BollyWoodobj,'homebollywoodproductobjrow2':homebollywoodproductobjrow2, 'homebollywoodproductobjrow1':homebollywoodproductobjrow1}
        return render(request, 'core/home-screen.html',context)

class SelectYourAddress(View):
    def get(self, request):
        userobj, usertypeobj, LoginProfileobj= userprofile(request)
        catlevel1,catlevel2,catlevel3=category()
        cart_count=AddToCart.objects.filter(LoginId=userobj, MoneyStatus=0).count()
        context={'cart_count':cart_count,'cat1':catlevel1,'cat2':catlevel2,'cat3':catlevel3}
        return render(request, 'core/select-your-address-for-existing-user.html',context)

class SeeAllProducts(View):
    def get(self, request, slug):
        userobj, usertypeobj, LoginProfileobj= userprofile(request)
        catlevel1,catlevel2,catlevel3=category()
        cat3obj=CategoryLevel3.objects.get(CategorySlug=slug)
        productobj=Product.objects.filter(CategoryLevel3Id=cat3obj)
        colors=ProductColor.objects.all()
        brands=Product.objects.all()
        product=brands.values('ProductBrandName').distinct()
        print(product)
        size_obj=ProductSize.objects.all()
        print(colors)
        cart_count=AddToCart.objects.filter(LoginId=userobj, MoneyStatus=0).count()
        context={'cart_count':cart_count,'cat1':catlevel1,'cat2':catlevel2,'cat3':catlevel3,'product':productobj,'color_obj':colors, 'brands':product, 'size_obj':size_obj}
        return render(request, 'core/see-all-products.html',context)

class ProductDetail(View):
    def get(self, request,slug, id=None):
        productobj=Product.objects.get(ProductSlug=slug)
        user= request.user
        userobj, usertypeobj, LoginProfileobj= userprofile(request)
        # Address Show in Product Deatils
        try:
            address=Address.objects.filter(UserLoginProfileId=userobj).get(AddressStatus=True)
        except:
            address=None
        catlevel1,catlevel2,catlevel3=category()
        Productobject=ProductSizeColor.objects.filter(Product=productobj)
        if id != None:
            colour=ProductSizeColor.objects.get(id=id)
            z=Productobject.filter(ProductColour=colour.ProductColour)
            
            l=[]
            
            sizeobj=[]
            for i in z:
                sizeobj.append(i.ProductSize.size)
                # print('price', i.Price)
            sizeobj=list(set(sizeobj))
            
        else:
            sizeobj=[]
            for i in Productobject:
                sizeobj.append(i.ProductSize.size)
                # print('price', i.Price)
            sizeobj=list(set(sizeobj))
            
           
       
        ProductColourobj=Productobject.values_list('ProductColour', flat=True).distinct()
        ColourObj=ProductColor.objects.filter(pk__in=ProductColourobj)
        UniqueColourImage=[]
        for i in ColourObj:
            UniqueColourImage.append(Productobject.filter(ProductColour=i).last())
        QuestionsAndAnswersobj=QuestionsAndAnswers.objects.filter(ProductId=productobj.id)[:5]

        selctedsize=request.GET.get('size')
        if selctedsize:
            prosize=ProductSize.objects.get(size=selctedsize)
            obj=ProductSizeColor.objects.filter(Product=productobj).get(ProductSize=prosize)
            # print('obj',obj.discount)
        else:
            prosize=None
            obj=None
        
        reviews=Review_products.objects.filter(Cart=productobj)[:3]
        reviewcount=Review_products.objects.filter(Cart=productobj).count()


        reviewsforprogressbar=Rating_Product.objects.filter(Cart=productobj).count()
        rating_star=Rating_Product.objects.filter(Cart=productobj)
        
        fivestarcount=Rating_Product.objects.filter(Cart=productobj).filter(Rating_star=5).count()
        fourstarcount=Rating_Product.objects.filter(Cart=productobj).filter(Rating_star__gte=4,Rating_star__lte=4.9).count()
        threestarcount=Rating_Product.objects.filter(Cart=productobj).filter(Rating_star__gte=3,Rating_star__lte=3.9).count()
        twostarcount=Rating_Product.objects.filter(Cart=productobj).filter(Rating_star__gte=2,Rating_star__lte=2.9).count()
        onestarcount=Rating_Product.objects.filter(Cart=productobj).filter(Rating_star__gte=1,Rating_star__lte=1.9).count()



        
        try:
            fivestar=(int(Rating_Product.objects.filter(Cart=productobj).filter(Rating_star=5).count())//int(reviewsforprogressbar))*100
        except:
            fivestar=0
        try:
            fourstar=(int(Rating_Product.objects.filter(Cart=productobj).filter(Rating_star__gte=4,Rating_star__lte=4.9).count())//int(reviewsforprogressbar))*100
        except:
            fourstar=0
        try:
            threestar=(Rating_Product.objects.filter(Cart=productobj).filter(Rating_star__gte=3,Rating_star__lte=3.9).count()//int(reviewsforprogressbar))*100
        except:
            threestar=0
        try:
            twostar=(Rating_Product.objects.filter(Cart=productobj).filter(Rating_star__gte=2,Rating_star__lte=2.9).count()//int(reviewsforprogressbar))*100
        except:
            twostar=0
        try:
            onestar=(Rating_Product.objects.filter(Cart=productobj).filter(Rating_star__gte=1,Rating_star__lte=1.9).count()//int(reviewsforprogressbar))*100
        except:
            onestar=0
        
        cart_count=AddToCart.objects.filter(LoginId=userobj, MoneyStatus=0).count()
        context={'obj':obj,'cart_count':cart_count,'rating_star':rating_star,'reviewcount':reviewcount,'fivestarcount':fivestarcount,'fourstarcount':fourstarcount,'threestarcount':threestarcount,'twostarcount':twostarcount,'onestarcount':onestarcount,
                'onestar':onestar,'twostar':twostar,'threestar':threestar,'fourstar':fourstar ,'fivestar':fivestar,  'reviews':reviews,'cat1':catlevel1,'cat2':catlevel2,
                'cat3':catlevel3,'prosize':prosize,'slug':slug,'product':productobj,'Address_obj':address,'userobj':userobj,'QuestionsAndAnswersobj':QuestionsAndAnswersobj,'LoginProfileobj':LoginProfileobj,'id':id,
                'SizeObj_id':sizeobj,'UniqueColourImage':UniqueColourImage}
        return render(request, 'core/Deals-of-the-day-product-buy-screen.html',context)
    
    # def post(self, request,slug,id):
    #     userobj, usertypeobj, LoginProfileobj= userprofile(request)
    #     print(slug)
    #     x=request.POST.get('addressline1')
    #     address2=request.POST.get('addressline2')
    #     landmark=request.POST.get('landmark')
    #     city=request.POST.get('city')
    #     state=request.POST.get('state')
    #     addresstype=request.POST['selectaddresstype']
        
    #     defaultaddress=request.POST.get('defaultaddress')

    #     # defaultaddressobj=Address.objects.create(UserLoginProfileId=userobj,Address_line2=address2, 
    #     #                             Landmark=landmark, City=city, state=state, AddressType=addresstype)
    #     # if defaultaddress:
    #     #     obj=SetDefaultAddress()
    #     #     obj.get(request,defaultaddressobj.id)
    #     return redirect(f'/ProductDetail/{slug}')


# Edit Address
class EditAdress(View):
    @method_decorator(login_required(login_url='/signin'))
    def post(self, request, id):
        useraddress=Address.objects.get(id=id)
        useraddress.FullName=request.POST['fname']
        useraddress.MobileNo=request.POST['mnumber']
        useraddress.PinCode=request.POST['pincode']
        useraddress.Address_line1=request.POST['addressline1']
        useraddress.Address_line2=request.POST['addressline2']
        useraddress.Landmark=request.POST['landmark']
        useraddress.City=request.POST['city']
        useraddress.state=request.POST['state']
        useraddress.AddressType=request.POST['selectaddresstype']
        useraddress.save()
        return redirect("/saveaddress")

# Save multiple Address of users
class SaveAddress(View):
    @method_decorator(login_required(login_url='/signin'))
    def get(self, request):
        userobj, usertypeobj, LoginProfileobj= userprofile(request)
        catlevel1,catlevel2,catlevel3=category()
        multipleaddress=Address.objects.filter(UserLoginProfileId=request.user)
        addresscount=multipleaddress.count()
        if addresscount>1:
            yourotheraddress=True
        else:
            yourotheraddress=False
        cart_count=AddToCart.objects.filter(LoginId=userobj, MoneyStatus=0).count()
        context={'cart_count':cart_count,'yourotheraddress':yourotheraddress,'cat1':catlevel1,'cat2':catlevel2,'cat3':catlevel3,'multipleaddress':multipleaddress}
        return render(request, 'core/Save-address.html', context)   

    @method_decorator(login_required(login_url='/signin'))
    def post(self, request, slug=None):
        userobj, usertypeobj, LoginProfileobj= userprofile(request)
        fname=request.POST.get('fname')
        mnumber=request.POST.get('mnumber')
        pincode=request.POST.get('pincode')
        address1=request.POST.get('addressline1')
        address2=request.POST.get('addressline2')
        landmark=request.POST.get('landmark')
        city=request.POST.get('city')
        state=request.POST.get('state')
        addresstype=request.POST['selectaddresstype']
        defaultaddress=request.POST.get('defaultaddress')

        # # # print(defaultaddress)
        obj1= Address.objects.create(UserLoginProfileId=userobj,FullName=fname, MobileNo=mnumber, 
                                    PinCode=pincode, Address_line1= address1, Address_line2=address2, 
                                    Landmark=landmark, City=city, state=state, AddressType=addresstype)

        if defaultaddress:
            obj=SetDefaultAddress()
            obj.get(request,obj1.id)
        if slug!=None:
            return redirect(f'/ProductDetail/{slug}')
        else:
            return redirect('/saveaddress')

# Save Address From Product Detail Page
class SaveAddressFromDetailPage(View):
    @method_decorator(login_required(login_url='/signin'))
    def post(self, request):
        userobj, usertypeobj, LoginProfileobj= userprofile(request)
        fname=request.POST.get('fname')
        mnumber=request.POST.get('mnumber')
        pincode=request.POST.get('pincode')
        address1=request.POST.get('addressline1')
        address2=request.POST.get('addressline2')
        landmark=request.POST.get('landmark')
        city=request.POST.get('city')
        state=request.POST.get('state')
        addresstype=request.POST['selectaddresstype']
        defaultaddress=request.POST.get('defaultaddress')

        # # # print(defaultaddress)
        obj1= Address.objects.create(UserLoginProfileId=userobj,FullName=fname, MobileNo=mnumber, 
                                    PinCode=pincode, Address_line1= address1, Address_line2=address2, 
                                    Landmark=landmark, City=city, state=state, AddressType=addresstype)

        if defaultaddress:
            obj=SetDefaultAddress()
            obj.get(request,obj1.id)

        return redirect('/saveaddress')

class SetDefaultAddress(View):
    def get(self,request,id):
        userobj=request.user
        try:
            useraddress=Address.objects.filter(UserLoginProfileId=userobj).get(AddressStatus=True)
            useraddress.AddressStatus=False
            useraddress.save()
        except:
            pass
        useraddress=Address.objects.get(id=id)
        useraddress.AddressStatus=True
        useraddress.save()
        return redirect('/saveaddress')

from django.db.models import Sum
# ItemPrice.objects.aggregate(Sum('price'))
class AddToCard(View):
    @method_decorator(login_required(login_url='/signin'))
    def get(self, request,id=None):
        userobj, usertypeobj, LoginProfileobj= userprofile(request)
        catlevel1,catlevel2,catlevel3=category()
        TotalCartPrice=0
        TotalCartDiscount=0
        AddToCartobj= AddToCart.objects.filter(LoginId=request.user).filter(MoneyStatus=False)
        print(AddToCartobj,"yes")
        CartProductCount=AddToCartobj.filter(MoneyStatus=False).count()
        TotalCart=AddToCartobj.filter(MoneyStatus=False)

        addressobj=Address.objects.filter(UserLoginProfileId=request.user)
        defaultaddress=None

        for i in addressobj:
            if i.AddressStatus==True:
                defaultaddress=i
        # # # print(defaultaddress)

        for i in TotalCart:
            TotalCartPrice+=int(i.ProductSizeColorId.Price)
            TotalCartDiscount+=int(i.ProductSizeColorId.saved)

        TotalAmount= TotalCartPrice-TotalCartDiscount
        cart_count=AddToCart.objects.filter(LoginId=userobj, MoneyStatus=0).count()
        

        context={'Delivery_date':Delivery_date,'cart_count':cart_count,'defaultaddress':defaultaddress,'TotalAmount':TotalAmount,'TotalCartDiscount':TotalCartDiscount,'TotalCartPrice':TotalCartPrice,'CartProductCount':CartProductCount,'cat1':catlevel1,'cat2':catlevel2,'cat3':catlevel3,'AddToCartobj':AddToCartobj}
        return render(request, 'core/add-to-card.html', context)
    
    @method_decorator(login_required(login_url='/signin'))
    def post(self, request, id):
        userobj, usertypeobj, LoginProfileobj= userprofile(request)
        product_obj=Product.objects.get(id=id)
        color=request.POST['color']
        size=request.POST['size']
        quantity=request.POST['q']

        Product_color_obj=ProductColor.objects.get(ProductColorName=color)
        Product_Size_obj=ProductSize.objects.get(size=size)
        ProductColorImage_obj=ProductColourImage.objects.get(ProductColor=Product_color_obj)
      
        Product_obj_id=ProductSizeColor.objects.filter(Product=product_obj).filter(ProductColourImage=ProductColorImage_obj.id).get(ProductSize=Product_Size_obj)
        AddToCart.objects.create(ProductSizeColorId=product_obj,
                                LoginId=userobj,
                                Qunatity=quantity,
                                TotalPrice=int(product_obj.Price)*quantity,)
        
        return redirect(f'/add-to-card')

class AddressSave(View):
    def get(self, request):
        return render(request, 'core/address-save.html')
     
class BuyNow(View):
    def get(self, request, id=None):
        userobj, usertypeobj, LoginProfileobj= userprofile(request)
        catlevel1,catlevel2,catlevel3=category()
        if id != None:
            AddToCartobj=AddToCart.objects.get(id=id)
            Total_price_without_discount=AddToCartobj.ProductSizeColorId.Price
            Total_quantity=AddToCartobj.Qunatity
            Total_discount=AddToCartobj.ProductSizeColorId.discount

            TotalPrice=Total_quantity*Total_price_without_discount
            # # print(TotalPrice)
            TotalAmount=Total_quantity*Total_discount
            # # print(TotalAmount)
            AddToCartobj.TotalPrice=TotalAmount
            AddToCartobj.save()
            TotalDiscountPrice= TotalPrice-TotalAmount
            # # print(TotalDiscountPrice)

        else:
            AddToCartobj=AddToCart.objects.filter(LoginId=request.user)
            TotalCart=AddToCartobj.filter(MoneyStatus=False)

            l=[]
            d=[]
            for i in TotalCart:
                l.append(int(i.Qunatity)*int(i.ProductSizeColorId.Price))
                d.append(int(i.ProductSizeColorId.discount)*int(i.Qunatity))

            
            TotalPrice=sum(l)
            TotalAmount=sum(d)

            # discount_ammount=int(TotalPrice-TotalAmount)
            # # # print(discount_ammount)
            

            TotalDiscountPrice= TotalPrice-TotalAmount

        addressobj=Address.objects.filter(UserLoginProfileId=request.user)
        defaultaddress=None

        for i in addressobj:
            if i.AddressStatus==True:
                defaultaddress=i
        otheraddress=addressobj.exclude(AddressStatus=True)
        Delivery_date=date.today() + timedelta(days=5)
        cart_count=AddToCart.objects.filter(LoginId=userobj, MoneyStatus=0).count()
        context={'Delivery_date':Delivery_date,'cart_count':cart_count,'id':id,'TotalAmount':TotalAmount,'TotalCartDiscount':TotalDiscountPrice,'TotalCartPrice':TotalPrice,'otheraddress':otheraddress,'defaultaddress':defaultaddress,'AddToCartobj':AddToCartobj,'cat1':catlevel1,'cat2':catlevel2,'cat3':catlevel3}
        return render(request, 'core/buy-now.html',context)

    def post(self, request, id):
        userobj, usertypeobj, LoginProfileobj= userprofile(request)
        print(id)
        Product_obj=Product.objects.get(id=id)
        size=ProductSize.objects.get(size=request.POST.get('size'))
        quantity=request.POST['q']
        
        product_obj=ProductSizeColor.objects.filter(Product=Product_obj).get(ProductSize=size.id)
        
        # product_obj=ProductSizeColor.objects.get(id=id)
        # quantity=request.POST['q']
        obj=AddToCart.objects.create(ProductSizeColorId=product_obj,
                                        LoginId=userobj,
                                        Qunatity=quantity,
                                        TotalPrice=0)
        # product_obj=Product.objects.get(id=id)

        # color=request.POST['color']
        # # print(color)
        # size=request.POST['size']
        # # print(size)
        # quantity=request.POST['q']
        # # print(quantity)

        # Product_color_obj=ProductColor.objects.get(ProductColorName=color)
        # Product_Size_obj=ProductSize.objects.get(size=size)
        # ProductColorImage_obj=ProductColourImage.objects.get(ProductColor=Product_color_obj)
        # Product_obj_id=ProductSizeColor.objects.filter(Product=product_obj).filter(ProductColourImage=ProductColorImage_obj.id).get(ProductSize=Product_Size_obj)

        # obj=AddToCart.objects.create(ProductSizeColorId=Product_obj_id,
        #                         LoginId=userobj,
        #                         Qunatity=quantity,
        #                         TotalPrice=0)
        return redirect(f"/buy-now/{obj.id}")

class ChooseLocation(View):
    def get(self, request):
        return render(request, 'core/choose-location.html')        

class PlaceOrder(View):
    def get(self, request):
        
        return render(request, 'core/place-order.html')     

# anushree changes
class SeeAll(View):
    def get(self, request,slug,slug1,slug2):
        userobj, usertypeobj, LoginProfileobj= userprofile(request)
        catlevel1,catlevel2,catlevel3=category()
        color_obj=ProductColor.objects.all()
        size_obj=ProductSize.objects.all()
        # brands=[]
        if slug1!=None and slug2!=None:
            cat3obj=CategoryLevel3.objects.get(CategorySlug=slug2)
            productobj=Product.objects.filter(CategoryLevel3Id=cat3obj)
            # brands1=Product.objects.all()
            product=productobj.values('ProductBrandName').distinct()
            print(product)
            Price=productobj.aggregate(Min('Price'), Max('Price'))
            print(Price)
            # brands=productobj.values('ProductBrandName')
            # price=productobj.values('Price')
            # print(brands,price)
           
            home_category=None
            
        else:
            print(slug)
            home_category=HomeCategory.objects.get(HomeCategorySlug=slug)
            print(home_category.id)
            productobj=HomeSubCategory.objects.filter(HomeCategory=home_category)
            product_id = productobj.values('ProductId')
            print(product_id)
            brands1=Product.objects.filter(id__in=product_id)
            product=brands1.values('ProductBrandName').distinct()
            print(product)
            Price=brands1.aggregate(Min('Price'), Max('Price'))
            print(Price)
            print('brands1',brands1)
            cat3obj = None

        cart_count=AddToCart.objects.filter(LoginId=userobj, MoneyStatus=0).count()
        context={'cart_count':cart_count,'cat3obj':cat3obj,'Price':Price,'brands':product,'home_category':home_category,'cat1':catlevel1,'cat2':catlevel2,'cat3':catlevel3,'data':productobj, 'color_obj':color_obj, 'size_obj':size_obj}
        return render(request, 'core/Deals-of-the-day-(see-all-product-page).html',context)

class AllQuestion(View):
    def get(self, request, slug):
        userobj, usertypeobj, LoginProfileobj= userprofile(request)
        catlevel1,catlevel2,catlevel3=category()
        productobj=Product.objects.get(ProductSlug=slug)
        QuestionsAndAnswersobj=QuestionsAndAnswers.objects.filter(ProductId=productobj)

        reviewsforprogressbar=Rating_Product.objects.filter(Cart=productobj).count()
        rating_star=Rating_Product.objects.filter(Cart=productobj)
        
        fivestarcount=Rating_Product.objects.filter(Cart=productobj).filter(Rating_star=5).count()
        fourstarcount=Rating_Product.objects.filter(Cart=productobj).filter(Rating_star__gte=4,Rating_star__lte=4.9).count()
        threestarcount=Rating_Product.objects.filter(Cart=productobj).filter(Rating_star__gte=3,Rating_star__lte=3.9).count()
        twostarcount=Rating_Product.objects.filter(Cart=productobj).filter(Rating_star__gte=2,Rating_star__lte=2.9).count()
        onestarcount=Rating_Product.objects.filter(Cart=productobj).filter(Rating_star__gte=1,Rating_star__lte=1.9).count()



        
        try:
            fivestar=(int(Rating_Product.objects.filter(Cart=productobj).filter(Rating_star=5).count())//int(reviewsforprogressbar))*100
        except:
            fivestar=0
        try:
            fourstar=(int(Rating_Product.objects.filter(Cart=productobj).filter(Rating_star__gte=4,Rating_star__lte=4.9).count())//int(reviewsforprogressbar))*100
        except:
            fourstar=0
        try:
            threestar=(Rating_Product.objects.filter(Cart=productobj).filter(Rating_star__gte=3,Rating_star__lte=3.9).count()//int(reviewsforprogressbar))*100
        except:
            threestar=0
        try:
            twostar=(Rating_Product.objects.filter(Cart=productobj).filter(Rating_star__gte=2,Rating_star__lte=2.9).count()//int(reviewsforprogressbar))*100
        except:
            twostar=0
        try:
            onestar=(Rating_Product.objects.filter(Cart=productobj).filter(Rating_star__gte=1,Rating_star__lte=1.9).count()//int(reviewsforprogressbar))*100
        except:
            onestar=0
        

        cart_count=AddToCart.objects.filter(LoginId=userobj, MoneyStatus=0).count()
        context={'cart_count':cart_count,'fivestarcount':fivestarcount,'fourstarcount':fourstarcount,'threestarcount':threestarcount,'twostarcount':twostarcount,'onestarcount':onestarcount,
                'onestar':onestar,'twostar':twostar,'threestar':threestar,'fourstar':fourstar ,'fivestar':fivestar,'cat1':catlevel1,'cat2':catlevel2,'cat3':catlevel3,'product':productobj,'QuestionsAndAnswersobj':QuestionsAndAnswersobj}
        return render(request, 'core/see-all-questions.html',context)

#Anushree Code
class AddToCartPage(View):
    @method_decorator(login_required(login_url='/signin'))
    def get(self,request,id=None):
        userobj, usertypeobj, LoginProfileobj= userprofile(request)
        catlevel1,catlevel2,catlevel3=category()
        # TotalCartPrice=0
        # TotalCartDiscount=0
        AddToCartobj= AddToCart.objects.filter(LoginId=request.user).filter(MoneyStatus=False)
        CartProductCount=AddToCartobj.filter(MoneyStatus=False).count()
        TotalCart=AddToCartobj.filter(MoneyStatus=False)

        addressobj=Address.objects.filter(UserLoginProfileId=request.user)
        defaultaddress=None

        for i in addressobj:
            if i.AddressStatus==True:
                defaultaddress=i
        # # # print(defaultaddress)

        l=[]
        d=[]
        for i in TotalCart:
            l.append(int(i.Qunatity)*int(i.ProductSizeColorId.Price))
            # print(i.TotalPrice)
            i.TotalPrice=int(i.ProductSizeColorId.discount)*int(i.Qunatity)
            i.save()
            d.append(int(i.ProductSizeColorId.discount)*int(i.Qunatity))

        
        TotalPrice=sum(l)
        TotalAmount=sum(d)
        # discount_ammount=int(TotalPrice-TotalAmount)
        # # # print(discount_ammount)
           

        TotalDiscountPrice= TotalPrice-TotalAmount
        cart_count=AddToCart.objects.filter(LoginId=userobj, MoneyStatus=0).count()
        Delivery_date=date.today() + timedelta(days=5)
        context={'Delivery_date':Delivery_date,'cart_count':cart_count,'defaultaddress':defaultaddress,'TotalAmount':TotalAmount,'TotalCartDiscount':TotalDiscountPrice,'TotalCartPrice':TotalPrice,'CartProductCount':CartProductCount,'cat1':catlevel1,'cat2':catlevel2,'cat3':catlevel3,'AddToCartobj':AddToCartobj}
        return render(request,'core/add-to-card1.html',context)

    @method_decorator(login_required(login_url='/signin'))
    def post(self, request, slug):
        userobj, usertypeobj, LoginProfileobj= userprofile(request)
        
        Product_obj=Product.objects.get(ProductSlug=slug)
        size=ProductSize.objects.get(size=request.POST.get('size'))
        quantity=request.POST['q']
        
        product_obj=ProductSizeColor.objects.filter(Product=Product_obj).get(ProductSize=size.id)
        print(product_obj)

        # print(Product_obj)
        # print(size.id)
        # product_obj=ProductSizeColor.objects.get(id=id)
        # # color=request.POST['color']
        # # size=request.GET['size']
        
        # 

        # print(color,size,quantity)

        # Product_color_obj=ProductColor.objects.get(ProductColorName=color)
        # Product_Size_obj=ProductSize.objects.get(size=size)
        # ProductColorImage_obj=ProductColourImage.objects.get(ProductColor=Product_color_obj)
        # for i in ProductColorImage_obj:
        #     # # print(i.id)
        # # print(ProductColorImage_obj.id)

        # Product_obj_id=ProductSizeColor.objects.filter(Product=product_obj).filter(ProductColourImage=ProductColorImage_obj.id).get(ProductSize=Product_Size_obj)
        # # print(Product_obj_id.discount)

        # for i in ProductColorImage_obj:
        #     # # print(i.ProductColor.ProductColorName)
        #     ProductSizeColor_obj=ProductSizeColor.objects.get(ProductColourImage=i.id)
        #     # # print(ProductSizeColor_obj.Price)
        # Product_obj_id=Product_obj_id.filter(ProductColourImage=ProductColorImage_obj)

        AddToCart.objects.create(ProductSizeColorId=product_obj,
                                LoginId=userobj,
                                Qunatity=quantity,
                                TotalPrice=0)

        return redirect(f'/AddToCart')

class RemoveIItemFromCart(View):
    def get(self, request, id):
        AddToCartobj=AddToCart.objects.get(id=id)
        AddToCartobj.delete()
        return redirect('/AddToCart')

#Anushree Code
class BuyNowNew(View):
    def get(self,request):
        return render(request,'core/buy-now1.html')

class PlaceOrderNew(View):
    def get(self,request, id=None):
        userobj, usertypeobj, LoginProfileobj= userprofile(request)
        catlevel1,catlevel2,catlevel3=category()
        multipleaddressplaceorder=Address.objects.filter(UserLoginProfileId=request.user)
        addresscount=multipleaddressplaceorder.count()
        if addresscount>1:
            yourotheraddress=True
        else:
            yourotheraddress=False
        try:
            address=Address.objects.filter(UserLoginProfileId=request.user).get(AddressStatus=True)
        except:
            address=None
        
        price=[]
        if id!=None:

            cart_obj=AddToCart.objects.get(id=id)
            cart_obj.delivry_address=address
            cart_obj.save()
            productprice=cart_obj.ProductSizeColorId.Price*cart_obj.Qunatity
            
            cart_Total=cart_obj.TotalPrice

        else:

            cart_obj=AddToCart.objects.filter(LoginId=request.user,MoneyStatus=False)
            # print(cart_obj)
            cart_Total=0
            for i in cart_obj:
                i.delivry_address=address
                i.save()
                cart_Total+=i.TotalPrice
                price.append(int(i.ProductSizeColorId.Price)*int(i.Qunatity))
            productprice=sum(price)

        product_discount=productprice-cart_Total

        cart_count=AddToCart.objects.filter(LoginId=userobj, MoneyStatus=0).count()
        context={'cart_count':cart_count,'addresscount':yourotheraddress,'id':id,'cart_Total':cart_Total,'productprice':productprice,'product_discount':product_discount,'cat1':catlevel1,'cat2':catlevel2,'cat3':catlevel3,'multipleaddressplaceorder':multipleaddressplaceorder}
        return render(request,'core/place-order1.html',context)

    def post(self,request):
        userobj, usertypeobj, LoginProfileobj= userprofile(request)
        fname=request.POST.get('fname')
        mnumber=request.POST.get('mnumber')
        pincode=request.POST.get('pincode')
        address1=request.POST.get('addressline1')
        address2=request.POST.get('addressline2')
        landmark=request.POST.get('landmark')
        city=request.POST.get('city')
        state=request.POST.get('state')
        addresstype=request.POST['selectaddresstype']
        defaultaddress=request.POST.get('defaultaddress')

        defaultaddressobj=Address.objects.create(UserLoginProfileId=userobj,FullName=fname, MobileNo=mnumber, 
                                    PinCode=pincode, Address_line1= address1, Address_line2=address2, 
                                    Landmark=landmark, City=city, state=state, AddressType=addresstype)

        if defaultaddress:
            obj=SetDefaultAddress()
            obj.get(request,defaultaddressobj.id)

        return redirect('/PlaceOrderNew')

class Order(View):
    @method_decorator(login_required(login_url='/signin'))
    def get(self,request):

        userobj, usertypeobj, LoginProfileobj= userprofile(request)

        catlevel1,catlevel2,catlevel3=category()
        order_id = request.GET.get('order_id')
        if request.GET.get('razorpay_order_id'):
            razorpay_order_id=request.GET.get('razorpay_order_id')
            razorpay_payment_id = request.GET.get('razorpay_payment_id')
            razorpay_signature = request.GET.get('razorpay_signature')

            # # print(razorpay_order_id)
            cart_obj=AddToCart.objects.filter(orderid=razorpay_order_id,LoginId=request.user)
            for i in cart_obj:
                i.MoneyStatus=1
                i.razor_pay_order_id=razorpay_order_id
                i.razor_pay_payment_id=razorpay_payment_id
                i.razor_pay_payment_signature=razorpay_signature
                i.OrderDate=date.today()
                i.Payment_method="PAID"
                i.save()
        else:
            cart_obj=AddToCart.objects.filter(LoginId=request.user)
        cart=AddToCart.objects.filter(LoginId=request.user, MoneyStatus=1)[::-1]

        for i in cart:
            if i.ReturnrequestbyDate !=None:
                if not datetime.strptime(str(i.ReturnrequestbyDate), '%Y-%m-%d')>datetime.today():
                    i.ReturnRequest = True

        Rating_Productobj=Rating_Product.objects.filter(login_id=request.user)
        cart_count=AddToCart.objects.filter(LoginId=userobj, MoneyStatus=0).count()
        context={'userobj':userobj,'cart_count':cart_count,'Rating_Productobj':Rating_Productobj,'cart':cart,'cat1':catlevel1,'cat2':catlevel2,'cat3':catlevel3}
        return render(request,'core/order.html', context)

    @method_decorator(login_required(login_url='/signin'))
    def post(self, request):
        userobj, usertypeobj, LoginProfileobj= userprofile(request)
        product=request.POST.get("product_id")
        if Review_products.objects.filter(login_id=userobj).filter(Cart=product):
            rate=Review_products.objects.filter(login_id=userobj).get(Cart=product)
            try:
                rate.Review=request.POST.get("review")
                Productobj=Product.objects.get(id=product)
                Productobj.TotalReviewCount=int(Productobj.TotalReviewCount)+1
                Productobj.save()
            except:
                pass

            try:
                rate.Image1=request.FILES.get("profileimage1")
            except:
                pass

            try:
                rate.Image2=request.FILES.get('profileimage2')
            except:
                pass
            rate.save()
            
        else:
            Productobj=Product.objects.get(id=product)
            Review=request.POST.get("review")
            Image1=request.FILES.get("profileimage1")
            Image2=request.FILES.get("profileimage2")

            if Image1!=None and Image2!=None:
                Review_products.objects.create(Cart=Productobj,login_id=request.user,Review=Review,Review_Date=datetime.today(),Image1=Image1,Image2=Image2)
            elif Image1!=None:
                Review_products.objects.create(Cart=Productobj,login_id=request.user,Review=Review,Review_Date=datetime.today(),Image1=Image1)
            elif Image2!=None:
                Review_products.objects.create(Cart=Productobj,login_id=request.user,Review=Review,Review_Date=datetime.today(),Image2=Image2)
            else:
                Review_products.objects.create(Cart=Productobj,login_id=request.user,Review=Review,Review_Date=datetime.today())

            Productobj.TotalReviewCount=int(Productobj.TotalReviewCount)+1
            Productobj.save()
        return redirect("Order")

class Rate(View):
    def post(self, request,id):

        print(id)
        login_obj=request.user
        productobj=Product.objects.get(id=id)
        rate=request.POST.get('rate')
        
        print(productobj)
        if Rating_Product.objects.filter(login_id=login_obj).filter(Cart=productobj):
            ratingobj=Rating_Product.objects.filter(login_id=login_obj).get(Cart=productobj)
            ratingobj.Rating_star=rate
            ratingobj.save()
            productobj.TotalRatingCount=int(productobj.TotalRatingCount)+1
            productobj.Star= round((float(productobj.Star)+float(rate))/2,2)
        else:
            Rating_Product.objects.create(Rating_star=rate,login_id=request.user,Cart=productobj)
            productobj.TotalRatingCount=int(productobj.TotalRatingCount)+1
            productobj.Star= round((float(productobj.Star)+float(rate))/2,2)
        
        productobj.save()
        return redirect('Order')

class CanceledProduct(View):
    def get(self, request, id):
        # print(id)
        cart=AddToCart.objects.get(id=id)
        cart.CancelledStatus=1
        cart.CancelDate=date.today()
        cart.save()
        return redirect("Order")

class SetDefaultAddressPlaceorder(View):
    def get(self,request, id):
        # # print(id)
        userobj=request.user
        try:
                useraddress=Address.objects.filter(UserLoginProfileId=userobj).get(AddressStatus=True)
                useraddress.AddressStatus=False
                useraddress.save()
        except:
             pass
        useraddress=Address.objects.get(id=id)
        useraddress.AddressStatus=True
        useraddress.save()
        return redirect('/PlaceOrderNew')

class UpadateCartProductQuantity(View):
    def get(self, request, id):
        updateCart=AddToCart.objects.get(id=id)
        quantity=request.GET.get('quantity')
        updateCart.Qunatity=quantity
        updateCart.save()
        return redirect("/AddToCart")

class UpadateBuyNowProductQuantity(View):
    def get(self, request, id):
        updateCart=AddToCart.objects.get(id=id)
        quantity=request.GET.get('quantity')
        updateCart.Qunatity=quantity
        updateCart.save()
        return redirect(f"/buy-now/{updateCart.id}")

class UpadateBuyNowProductQuantityAll(View):
    def get(self, request, id):
        updateCart=AddToCart.objects.get(id=id)
        quantity=request.GET.get('quantity')
        updateCart.Qunatity=quantity
        updateCart.save()
        return redirect(f"/buy-now")

#shilpa code
class TrendingMoviesAttire(View):
    def get(self,request):
        userobj, usertypeobj, LoginProfileobj= userprofile(request)
        catlevel1,catlevel2,catlevel3=category()
        BollyWoodCategoryobj=BollyWoodCategory.objects.last()
        BollyWoodSubCategoryobj=BollyWoodSubCategory.objects.all()
        cart_count=AddToCart.objects.filter(LoginId=userobj, MoneyStatus=0).count()
        context={'cart_count':cart_count,'BollyWoodSubCategoryobj':BollyWoodSubCategoryobj,'BollyWoodCategoryobj':BollyWoodCategoryobj,'cat1':catlevel1,'cat2':catlevel2,'cat3':catlevel3}
        return render(request,'core/trending-movies-attire.html',context)        

class PaymenMethod(View):
    def get(self, request, id=None):
        userobj, usertypeobj, LoginProfileobj= userprofile(request)
        catlevel1,catlevel2,catlevel3=category()

        # random captcha
        lower='abcdefghijklmnopqrstuvwxyz'
        upper='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        number='0123456789'
        symbol='[]{}()#*;$&-_'

        all=lower+upper+number+symbol

        length=5
        captcha="".join(random.sample(all,length))

        # print(captcha)


        price=[]
        if id!=None:
            cart_obj=AddToCart.objects.get(id=id)
            productprice=cart_obj.ProductSizeColorId.Price*cart_obj.Qunatity
            
            cart_Total=cart_obj.TotalPrice
        else:
            cart_obj=AddToCart.objects.filter(LoginId=request.user,MoneyStatus=False)
            # print(cart_obj)
            cart_Total=0
            for i in cart_obj:
                # print(i.TotalPrice)
                cart_Total+=i.TotalPrice
                price.append(int(i.ProductSizeColorId.Price)*int(i.Qunatity))
                # productquantity
            # print(cart_Total)
            productprice=sum(price)
        product_discount=productprice-cart_Total
        client = razorpay.Client(auth = (settings.KEY,settings.SECREATE))
        # print(client)
        payment= client.order.create({'amount': cart_Total*100, 'currency':'INR', 'payment_capture':1 })
        # print(payment)
        if id!=None:
            cart_obj.orderid=payment['id']
            cart_obj.save()
        else:
            for j in cart_obj:
                j.orderid=payment['id']
                j.save()
        cart_count=AddToCart.objects.filter(LoginId=userobj, MoneyStatus=0).count()
        context={'cart_count':cart_count,'captcha':captcha,'cat1':catlevel1,'cat2':catlevel2,'cat3':catlevel3,'payment':payment,'id':id,'cart_Total':cart_Total,'productprice':productprice,'product_discount':product_discount,}
        return render(request,'core/continue-choose-payment-mode.html',context)

    def post(self, request, id=None):
        
        # random captcha
        lower='abcdefghijklmnopqrstuvwxyz'
        upper='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        number='0123456789'
        # symbol='[]{}()#*;$&-_'

        all=lower+upper+number


        length=14
        Oredr_id="".join(random.sample(all,length))
        # print(Oredr_id)

        # Cart=request.POST.get("cart_id")
        captcha_default=request.POST.get("captcha")
        User_captcha=request.POST.get("captcha_user")
        

        print(captcha_default)
        print(User_captcha)

        if (User_captcha==captcha_default):
            if id!=None:
                cart_obj=AddToCart.objects.get(id=id)
                cart_obj.MoneyStatus=1
                cart_obj.OrderDate=date.today()
                cart_obj.Payment_method="COD"
                cart_obj.save()
            else:
                cart_obj=AddToCart.objects.filter(LoginId=request.user,MoneyStatus=False)
                for i in cart_obj:
                    i.MoneyStatus=1
                    i.OrderDate=date.today()
                    i.Payment_method="COD"
                    i.save()
        else:
            print("No")
        
        return redirect("Order")

#Anushree Code
def error_404(request, exception=None):
        data = {}
        return render(request,'Core/Error.html', data)

#saveaddress pagedeco
def remove_row(request,id):
    # print(id)
    obj=Address.objects.get(id=id)
    obj.delete()
    return redirect('/saveaddress')

#place order new
def remove_row_placeOrder(request,id):
    # print(id)
    obj=Address.objects.get(id=id)
    obj.delete()
    return redirect('/PlaceOrderNew')

#place order new page
class EditAdressPlaceOrder(View):
    @method_decorator(login_required(login_url='/signin'))
    def post(self, request, id):
        useraddress=Address.objects.get(id=id)
        useraddress.FullName=request.POST['fname']
        useraddress.MobileNo=request.POST['mnumber']
        useraddress.PinCode=request.POST['pincode']
        useraddress.Address_line1=request.POST['addressline1']
        useraddress.Address_line2=request.POST['addressline2']
        useraddress.Landmark=request.POST['landmark']
        useraddress.City=request.POST['city']
        useraddress.state=request.POST['state']
        useraddress.AddressType=request.POST['selectaddresstype']
        useraddress.save()
        return redirect("/PlaceOrderNew")

class Orderexchange(View):
    def get(self, request):
        return render (request, "Core/order-exchange-same-item-with-different-size.html")   

class Ordersucessful(View):
    def get(self, request):
        return render(request, "Core/ordersuccessful.html")

class LikeQuestionAnswer(View):
    def post(self, request):
        userobj, usertypeobj, LoginProfileobj= userprofile(request)
        if request.method=="POST":
            question=QuestionsAndAnswers.objects.get(id=request.POST.get("question_id"))
            print(question)
            is_dislike = False
            for dislike in question.dislikes.all():
                if dislike == userobj:
                    is_dislike = True
                    break
            if is_dislike:
                question.dislikes.remove(userobj)
            is_like = False

            for like in question.likes.all():
                if like == userobj:
                    is_like = True
                    break

            if not is_like:
                question.likes.add(userobj)

            if is_like:
                question.likes.remove(userobj)

            # data={
            #     'question': question.likes.all().count()
            # }
            # return JsonResponse(data, safe=False)
        # return redirect(f'/ProductDetail/{question.ProductId.ProductSlug}')
        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

class Un_LikeQuestionAnswer(View):
    def post(self, request):
        userobj, usertypeobj, LoginProfileobj= userprofile(request)
        if request.method=="POST":
            question=QuestionsAndAnswers.objects.get(id=request.POST.get("question_obj"))
            


            is_like = False

            for like in question.likes.all():
                if like == userobj:
                    is_like = True
                    break

            if is_like:
                question.likes.remove(userobj)




            is_dislike = False
            
            for dislike in question.dislikes.all():
                if dislike == userobj:
                    is_dislike = True
                    break
            
            if not is_dislike:
                question.dislikes.add(userobj)

            if is_dislike:
                question.dislikes.remove(userobj)


            # if userobj in question.dislikes.all():
            #     question.dislikes.remove(userobj)
            # else:
            #     question.dislikes.add(userobj)
            #     print('unliked',question)

            # data={
            #     'question': question.dislikes.all().count()
            # }
            # return JsonResponse(data, safe=False)
        # return redirect(f'/ProductDetail/{question.ProductId.ProductSlug}')
        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

#Sawan code
class SeeAllPhotosVideos(View):
    def get(self, request, slug):
        userobj, usertypeobj, LoginProfileobj= userprofile(request)
        productobj=Product.objects.get(ProductSlug=slug)
        Review_productsobj=Review_products.objects.filter(Cart=productobj)
        catlevel1,catlevel2,catlevel3=category()
        cart_count=AddToCart.objects.filter(LoginId=userobj, MoneyStatus=0).count()
        context={'cart_count':cart_count,'cat1':catlevel1,'cat2':catlevel2,'cat3':catlevel3,'Review_productsobj':Review_productsobj}
        return render(request, 'core/see-all-customers-photos_and-videos.html',context)

from django.template.loader import render_to_string
class filterdata(View):
    def get(self,request, slug):
        product=request.GET.getlist('product[]')
        star = request.GET.get('star[]')
        print('star',star)
        print(type(star))
        minPrice=request.GET['minPrice']
        maxPrice=request.GET['maxPrice']
        if CategoryLevel3.objects.filter(CategorySlug=slug):
            Cat3=CategoryLevel3.objects.get(CategorySlug=slug)
            allproducts=Product.objects.filter(CategoryLevel3Id=Cat3)
        else:
            home=HomeCategory.objects.get(HomeCategorySlug=slug)
            productobj=HomeSubCategory.objects.filter(HomeCategory=home)
            product_id = productobj.values('ProductId')
            allproducts=Product.objects.filter(id__in=product_id)
        if len(product)>0:
            allproducts=allproducts.filter(ProductBrandName__in=product)
        # if len(star)>0:
        if star!=None:
            allproducts=allproducts.filter(Star__gte=star)
        print('allproducts',allproducts)
        allproducts=allproducts.filter(Price__gte=minPrice)
        allproducts=allproducts.filter(Price__lte=maxPrice)
        template=render_to_string('ajax/product-list.html', {'data':allproducts})
        return JsonResponse({'data':template})

#Anushree Code 
class MenCategoryMobile(View):
    def get(self, request,slug):
        userobj, usertypeobj, LoginProfileobj= userprofile(request)
        cat1=CategoryLevel1.objects.get(CategorySlug=slug)
        cat2=CategoryLevel2.objects.filter(CategoryLevel1Id=cat1)
        cart_count=AddToCart.objects.filter(LoginId=userobj, MoneyStatus=0).count()
        context={'cart_count':cart_count,'cat1':cat1,'cat2':cat2}
        return render(request, 'core/men-category-mobile.html',context)

class TopwearMobile(View):
    def get(self, request,slug):
        userobj, usertypeobj, LoginProfileobj= userprofile(request)
        cat2=CategoryLevel2.objects.get(CategorySlug=slug)
        cat3=CategoryLevel3.objects.filter(CategoryLevel2Id=cat2)
        cart_count=AddToCart.objects.filter(LoginId=userobj, MoneyStatus=0).count()
        context={'cart_count':cart_count,'cat2':cat2,'cat3':cat3}
        return render(request, 'core/topwear-mobile.html',context)

# -- Faq --
class Faq(View):
    def get(self, request):
        return render(request, 'core/FAQ.html')

# -- return-and-refund-policy --
class loadReturnRefundPolicy(View):
    def get(self, request):
        return render(request, 'core/return-and-refund-policy.html')

# -- privacy-policy --
class loadPrivacyPolicy(View):
    def get(self, request):
        return render(request, 'core/privacy-policy.html')

# -- term-and-conditions --
class loadTermAndConditions(View):
    def get(self, request):
        return render(request, 'core/term-and-conditions.html')

# -- become-supplier --
class loadBecomeSupplier(View):
    def get(self, request):
        userobj, usertypeobj, LoginProfileobj= userprofile(request)
        catlevel1, catlevel2, catlevel3 = category()
        cart_count=AddToCart.objects.filter(LoginId=userobj, MoneyStatus=0).count()
        context={'cart_count':cart_count,'cat1': catlevel1, 'cat2': catlevel2,
                   'cat3': catlevel3}
        return render(request, 'core/become-supplier.html', context)

# -- earn-scroly --
class loadEarnScroly(View):
    def get(self, request):
        userobj, usertypeobj, LoginProfileobj= userprofile(request)
        catlevel1, catlevel2, catlevel3 = category()
        cart_count=AddToCart.objects.filter(LoginId=userobj, MoneyStatus=0).count()
        context={'cart_count':cart_count,'cat1': catlevel1, 'cat2': catlevel2,
                   'cat3': catlevel3}
        return render(request, 'core/earn-scroly.html', context)

class SearchProduct(View):
    def get(self, request):
        userobj, usertypeobj, LoginProfileobj= userprofile(request)
        catlevel1,catlevel2,catlevel3=category()
        Value=request.GET.get('search')
        print(Value)
        productobj=Product.objects.filter(ProductName=Value)
        home_category=None
        brands=Product.objects.all()
        cart_count=AddToCart.objects.filter(LoginId=userobj, MoneyStatus=0).count()
        context={'cart_count':cart_count,'home_category':home_category,'cat1':catlevel1,'cat2':catlevel2,'cat3':catlevel3,'data':productobj,'brands':brands}
        return render(request, 'core/Deals-of-the-day-(see-all-product-page).html',context)

# -- see All reviews --
class loadSeeAllRevies(View):
    def get(self, request,slug):
        userobj, usertypeobj, LoginProfileobj= userprofile(request)
        catlevel1, catlevel2, catlevel3 = category()
        productobj=Product.objects.get(ProductSlug=slug)
        reviews=Review_products.objects.filter(Cart=productobj)
        reviewcount=Review_products.objects.filter(Cart=productobj).count()


        reviewsforprogressbar=Rating_Product.objects.filter(Cart=productobj).count()
        rating_star=Rating_Product.objects.filter(Cart=productobj)
        
        fivestarcount=Rating_Product.objects.filter(Cart=productobj).filter(Rating_star=5).count()
        fourstarcount=Rating_Product.objects.filter(Cart=productobj).filter(Rating_star__gte=4,Rating_star__lte=4.9).count()
        threestarcount=Rating_Product.objects.filter(Cart=productobj).filter(Rating_star__gte=3,Rating_star__lte=3.9).count()
        twostarcount=Rating_Product.objects.filter(Cart=productobj).filter(Rating_star__gte=2,Rating_star__lte=2.9).count()
        onestarcount=Rating_Product.objects.filter(Cart=productobj).filter(Rating_star__gte=1,Rating_star__lte=1.9).count()

        try:
            fivestar=(int(Rating_Product.objects.filter(Cart=productobj).filter(Rating_star=5).count())//int(reviewsforprogressbar))*100
        except:
            fivestar=0
        try:
            fourstar=(int(Rating_Product.objects.filter(Cart=productobj).filter(Rating_star__gte=4,Rating_star__lte=4.9).count())//int(reviewsforprogressbar))*100
        except:
            fourstar=0
        try:
            threestar=(Rating_Product.objects.filter(Cart=productobj).filter(Rating_star__gte=3,Rating_star__lte=3.9).count()//int(reviewsforprogressbar))*100
        except:
            threestar=0
        try:
            twostar=(Rating_Product.objects.filter(Cart=productobj).filter(Rating_star__gte=2,Rating_star__lte=2.9).count()//int(reviewsforprogressbar))*100
        except:
            twostar=0
        try:
            onestar=(Rating_Product.objects.filter(Cart=productobj).filter(Rating_star__gte=1,Rating_star__lte=1.9).count()//int(reviewsforprogressbar))*100
        except:
            onestar=0
        cart_count=AddToCart.objects.filter(LoginId=userobj, MoneyStatus=0).count()

        context={
            'cart_count':cart_count,'cat1': catlevel1, 'cat2': catlevel2, 'cat3': catlevel3,'reviews':reviews,'reviewcount':reviewcount,
            'rating_star':rating_star,'fivestarcount':fivestarcount,'fourstarcount':fourstarcount,'threestarcount':threestarcount,
            'twostarcount':twostarcount,'onestarcount':onestarcount,'onestar':onestar,'twostar':twostar,'threestar':threestar,'fourstar':fourstar ,
            'fivestar':fivestar,'productobj':productobj,'reviewsforprogressbar':reviewsforprogressbar
        }
        return render(request, 'core/see-all-reviews.html', context)

class LikeReview(View):
    def post(self, request):
        userobj, usertypeobj, LoginProfileobj= userprofile(request)
        if request.method=="POST":
            review=Review_products.objects.get(id=request.POST.get("review_id"))
            print(review)
            is_dislike = False
            for dislike in review.dislikes.all():
                if dislike == userobj:
                    is_dislike = True
                    break
            if is_dislike:
                review.dislikes.remove(userobj)
            is_like = False

            for like in review.likes.all():
                if like == userobj:
                    is_like = True
                    break

            if not is_like:
                review.likes.add(userobj)

            if is_like:
                review.likes.remove(userobj)

            # data={
            #     'question': question.likes.all().count()
            # }
            # return JsonResponse(data, safe=False)
        # return redirect(f'/ProductDetail/{question.ProductId.ProductSlug}')
        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

class Un_LikeReview(View):
    def post(self, request):
        userobj, usertypeobj, LoginProfileobj= userprofile(request)
        if request.method=="POST":
            review=Review_products.objects.get(id=request.POST.get("review_obj"))
            


            is_like = False

            for like in review.likes.all():
                if like == userobj:
                    is_like = True
                    break

            if is_like:
                review.likes.remove(userobj)




            is_dislike = False
            
            for dislike in review.dislikes.all():
                if dislike == userobj:
                    is_dislike = True
                    break
            
            if not is_dislike:
                review.dislikes.add(userobj)

            if is_dislike:
                review.dislikes.remove(userobj)


            # if userobj in question.dislikes.all():
            #     question.dislikes.remove(userobj)
            # else:
            #     question.dislikes.add(userobj)
            #     print('unliked',question)

            # data={
            #     'question': question.dislikes.all().count()
            # }
            # return JsonResponse(data, safe=False)
        # return redirect(f'/ProductDetail/{question.ProductId.ProductSlug}')
        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

# -- load Notification --
class loadNotification(View):
    def get(self, request):
        userobj, usertypeobj, LoginProfileobj= userprofile(request)
        catlevel1, catlevel2, catlevel3 = category()
        cart_count=AddToCart.objects.filter(LoginId=userobj, MoneyStatus=0).count()
        context={'cart_count':cart_count,'cat1': catlevel1, 'cat2': catlevel2,
                   'cat3': catlevel3}
        return render(request, 'core/notification.html', context)

class ReturnOrder(View):
    def get(self, request,id):
        userobj, usertypeobj, LoginProfileobj= userprofile(request)
        catlevel1,catlevel2,catlevel3=category()
        AddToCartobj=AddToCart.objects.get(id=id)
        cart_count=AddToCart.objects.filter(LoginId=userobj, MoneyStatus=0).count()
        context={'cart_count':cart_count,'AddToCartobj':AddToCartobj,'cat1':catlevel1,'cat2':catlevel2,'cat3':catlevel3}
        return render (request, "Core/return-order-screen.html",context)
    
    def post(self, request, id):
        userobj, usertypeobj, LoginProfileobj= userprofile(request)
        AddToCartobj=AddToCart.objects.get(id=id)
        reason=request.POST.get("flexRadioDefault")
        description=request.POST.get("message")
        print('AddToCartobj',AddToCartobj.id)
        print('reason',reason)
        print('description',description)
        if Return_Product.objects.filter(login=userobj).filter(ProductId=AddToCartobj):
            print("this product request already exits")
            return redirect(f'/ReturnOrder/{id}')
        else:
            Return_Product.objects.create(
                ProductId=AddToCartobj,login=userobj,Reason=reason,Message=description,
                Date=date.today()
            )
            AddToCartobj.ReturnRequest=1
            AddToCartobj.save()
            return redirect('Return_submit')

class Return_submit(View):
    def get(self, request):
        catlevel1,catlevel2,catlevel3=category()
        userobj, usertypeobj, LoginProfileobj= userprofile(request)
        Return_obj=Return_Product.objects.filter(login=userobj).last()
        print(Return_obj)
        cart_count=AddToCart.objects.filter(LoginId=userobj, MoneyStatus=0).count()
        context={'cart_count':cart_count,'cat1':catlevel1,'cat2':catlevel2,'cat3':catlevel3,'Return_obj':Return_obj}
        return render (request, "Core/Return_request-submitted.html",context)



def aboutus(request):
    return render(request,'Core/About-us.html')