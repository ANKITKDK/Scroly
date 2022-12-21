
from unicodedata import name
from django.urls import path

from .import views
from .import SupperuserAccountViews
from .import AdminAccoutViews


urlpatterns = [
    path('Base',views.Base.as_view(),name='Base'),
    path('Index',views.Index.as_view(),name='Index'),
    path('SubCategory',views.SubCategory.as_view(),name='SubCategory'),
    # path('NewOrder',views.NewOrder.as_view(),name='NewOrder'),
    path('OrderHistory',views.OrderHistory.as_view(),name='OrderHistory'),
    path('ReviewList',views.ReviewList.as_view(),name='ReviewList'),
    # path('UserCard',views.UserCard.as_view(),name='UserCard'),
    # path('UserProfile',views.UserProfile.as_view(),name='UserProfile'),
    path('VendorCard',views.VendorCard.as_view(),name='VendorCard'),
    path('VendorList',views.VendorList.as_view(),name='VendorList'),
    path('Vendorprofile',views.Vendorprofile.as_view(),name='Vendorprofile'),
    path('BrandList',views.BrandList.as_view(),name='BrandList'),
    path('Invoice',views.Invoice.as_view(),name='Invoice'),

# -----------------------------------SupperUserAccount----------------------------------------
    # path('SupperUserSignIn',SupperuserAccountViews.SupperUserSignIn.as_view(),name='SupperUserSignIn'),
    path('SupperUserDashboard',SupperuserAccountViews.SupperUserDashboard.as_view(),name='SupperUserDashboard'),
    path('AdminList',SupperuserAccountViews.AdminList.as_view(),name='AdminList'),
    path('UpdateAdminList/<int:id>',SupperuserAccountViews.UpdateAdminList.as_view(),name='UpdateAdminList'),
    path('AdminListDetails',SupperuserAccountViews.AdminListDetails.as_view(),name='AdminListDetails'),
    path("Block_AdminUser/<int:id>",SupperuserAccountViews.Block_AdminUser.as_view(),name="Block_AdminUser"),
    path("Unblock_AdminUser/<int:id>",SupperuserAccountViews.Unblock_AdminUser.as_view(),name="Unblock_AdminUser"),

# -----------------------------------AdminAccount----------------------------------------
    path('AdminSignIn',AdminAccoutViews.AdminSignIn.as_view(),name='AdminSignIn'),
    path('AdminDashboard',AdminAccoutViews.AdminDashboard.as_view(),name='AdminDashboard'),
    path('LogoutAdmin',AdminAccoutViews.LogoutAdmin.as_view(),name='LogoutAdmin'),
    path('Category1',AdminAccoutViews.Category1.as_view(),name='Category1'),
    path('UpdateCategory1/<int:id>',AdminAccoutViews.UpdateCategory1.as_view(),name='UpdateCategory1'),
    path('DeleteCategory1/<int:id>',AdminAccoutViews.DeleteCategory1.as_view(),name='DeleteCategory1'),
    path('Category2',AdminAccoutViews.Category2.as_view(),name='Category2'),
    path('UpdateCategory2/<int:id>',AdminAccoutViews.UpdateCategory2.as_view(),name='UpdateCategory2'),
    path('DeleteCategory2/<int:id>',AdminAccoutViews.DeleteCategory2.as_view(),name='DeleteCategory2'),
    path('Category3',AdminAccoutViews.Category3.as_view(),name='Category3'),
    path('UpdateCategory3/<int:id>',AdminAccoutViews.UpdateCategory3.as_view(),name='UpdateCategory3'),
    path('DeleteCategory3/<int:id>',AdminAccoutViews.DeleteCategory3.as_view(),name='DeleteCategory3'),
    
    path('AddProduct',AdminAccoutViews.AddProduct.as_view(),name='AddProduct'),
    path('AddProductColourImage',AdminAccoutViews.AddProductColourImage.as_view(),name='AddProductColourImage'),
    path('UpdateProductColourImage/<int:id>',AdminAccoutViews.UpdateProductColourImage.as_view(),name='UpdateProductColourImage'),
    path('DeleteProductColourImage/<int:id>',AdminAccoutViews.DeleteProductColourImage.as_view(),name='DeleteProductColourImage'),
    
    path('AddColor',AdminAccoutViews.AddColor.as_view(),name='AddColors'),
    path('UpdateColor/<int:id>',AdminAccoutViews.UpdateColor.as_view(),name='UpdateColor'),
    path('DeleteColor/<int:id>',AdminAccoutViews.DeleteColor.as_view(),name='DeleteColor'),
    path('AddSize',AdminAccoutViews.AddSize.as_view(),name='AddSize'),
    path('UpdateSize/<int:id>',AdminAccoutViews.UpdateSize.as_view(),name='UpdateSize'),
    path('DeleteSize/<int:id>',AdminAccoutViews.DeleteSize.as_view(),name='DeleteSize'),
   
    path('ProductList',AdminAccoutViews.ProductList.as_view(),name='ProductList'),
    path('UpdateProductList/<int:id>',AdminAccoutViews.UpdateProductList.as_view(),name='UpdateProductList'),
    path('UpdateProductList/<slug:slug>',AdminAccoutViews.UpdateProductList.as_view(),name='UpdateProductList'),
    path('DeleteProductList/<int:id>',AdminAccoutViews.DeleteProductList.as_view(),name='DeleteProductList'),
    path('ProductManage',AdminAccoutViews.ProductManage.as_view(),name='ProductManage'),
    path('ProductDetailAdmins/<slug:slug>',AdminAccoutViews.ProductDetail.as_view(),name='ProductDetailAdmins'),
    path('UpdateProductDetails/<int:id>',AdminAccoutViews.UpdateProductDetails.as_view(),name='UpdateProductDetails'),
    path('DeleteProductDetails/<int:id>',AdminAccoutViews.DeleteProductDetails.as_view(),name='DeleteProductDetails'),
    path('ProductGride',AdminAccoutViews.ProductGride.as_view(),name='ProductGride'),
    path('Product_Details/<int:id>',AdminAccoutViews.Product_Details.as_view(),name='Product_Details'),
    path('UpdateProductImage/<slug:slug>',AdminAccoutViews.UpdateProductImage.as_view(),name='UpdateProductImage'),



    path('NoramlUserList',AdminAccoutViews.NoramlUserList.as_view(),name='NoramlUserList'),
    path('Block_NormalUser/<int:id>',AdminAccoutViews.Block_NormalUser.as_view(),name='Block_NormalUser'),
    path('Unblock_NormalUser/<int:id>',AdminAccoutViews.Unblock_NormalUser.as_view(),name='Unblock_NormalUser'),
    path('NoramlUserList',AdminAccoutViews.NoramlUserList.as_view(),name='NoramlUserList'),
    path('NormalUserProfile/<int:id>',AdminAccoutViews.NormalUserProfile.as_view(),name='NormalUserProfile'),
   

    path('HomeCategory',AdminAccoutViews.HomeCategoryView.as_view(),name='HomeCategory'),
    path('HomeCategory/<int:id>',AdminAccoutViews.HomeCategoryView.as_view(),name='HomeCategory'),

    # Dhanashree changes
    path('HomeBanner',AdminAccoutViews.HomeBannerView.as_view(),name='HomeBanner'),
    path('DeteleHomeBanner/<int:id>',AdminAccoutViews.DeteleHomeBanner.as_view(),name='DeteleHomeBanner'),

    



    # Anushree Changes

    path('Questionandanswer/<slug:slug>',AdminAccoutViews.Questionandanswer.as_view(),name='questionandanswer'),
    path('UpdateQuestionAndAnswer/<int:id>',AdminAccoutViews.UpdateQuestionAndAnswer.as_view(),name='UpdateQuestionAndAnswer'),
    path('DeleteQuestionAndAnswer/<int:id>',AdminAccoutViews.DeleteQuestionAndAnswer.as_view(),name='DeleteQuestionAndAnswer'),
    

    

    # path('AddProductColour',AdminAccoutViews.AddProductColour.as_view(),name='AddProductColour'),

    #Anushree code
    path('HomeProduct',AdminAccoutViews.HomeProduct.as_view(),name='HomeProduct'),
    path('UpdateHomeProduct/<int:id>',AdminAccoutViews.UpdateHomeProduct.as_view(),name='UpdateHomeProduct'),
    path('DeleteHomeProduct/<int:id>',AdminAccoutViews.DeleteHomeProduct.as_view(),name='DeleteHomeProduct'),

    path('HomeBollyWood',AdminAccoutViews.HomeBollyWood.as_view(),name='HomeBollyWood'),
    path('DeleteHomeBollyWood/<int:id>',AdminAccoutViews.DeleteHomeBollyWood.as_view(),name='DeleteHomeBollyWood'),
   
    path('HomeBollyWoodProduct',AdminAccoutViews.HomeBollyWoodProduct.as_view(),name='HomeBollyWoodProduct'),
    path('DeleteHomeBollyWoodProduct/<int:id>',AdminAccoutViews.DeleteHomeBollyWoodProduct.as_view(),name='DeleteHomeBollyWoodProduct'),

    
    path('NewOrder',AdminAccoutViews.NewOrder.as_view(),name='NewOrder'),
    path('NewOrder/<int:id>',AdminAccoutViews.NewOrder.as_view(),name='NewOrder'),

    path('Return_Order',AdminAccoutViews.Return_Order.as_view(),name='Return_Order'),
    path('Return_Order/<int:id>',AdminAccoutViews.Return_Order.as_view(),name='Return_Order'),
]
