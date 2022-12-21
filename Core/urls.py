from django.urls import path
from .import views


urlpatterns = [
    # shilpa code
    path('base1',views.base1.as_view(),name='base1'),
    path('base2',views.base2.as_view(),name='base2'),
    path('',views.Home.as_view(),name='home'),
    path('SelectYourAddress',views.SelectYourAddress.as_view(),name='SelectYourAddress'),
    path('SeeAllProducts/<slug:slug>',views.SeeAllProducts.as_view(),name='SeeAllProducts'),
    path('ProductDetail/<slug:slug>',views.ProductDetail.as_view(),name='ProductDetail'),

    # newely added page
  
    
    path('address-save',views.AddressSave.as_view(),name="AddressSave"),
    path('saveaddress',views.SaveAddress.as_view(),name="saveaddress"),
    path('saveaddress/<slug:slug>',views.SaveAddress.as_view(),name="saveaddress"),
    path('EditAdress/<int:id>',views.EditAdress.as_view(),name="EditAdress"),
    path('buy-now/<int:id>',views.BuyNow.as_view(),name="BuyNow"),
    path('buy-now',views.BuyNow.as_view(),name="BuyNow"),
    path('choose-location',views.ChooseLocation.as_view(),name="ChooseLocation"),
    path('place-order',views.PlaceOrder.as_view(),name="PlaceOrder"),

    #Anushree code
    path('SeeAll/<slug:slug>/<slug:slug1>/<slug:slug2>',views.SeeAll.as_view(),name="SeeAll"),
    path('SeeAll/<slug:slug>',views.SeeAll.as_view(),name="SeeAll"),
    path('SetDefaultAddress/<int:id>',views.SetDefaultAddress.as_view(),name="SetDefaultAddress"),
    path('AllQuestion/<slug:slug>',views.AllQuestion.as_view(),name="AllQuestion"),


    path('ProductDetail/<slug:slug>/<int:id>',views.ProductDetail.as_view(),name='ProductDetail'),
    
    path('RemoveIItemFromCart/<int:id>',views.RemoveIItemFromCart.as_view(),name='RemoveIItemFromCart'),
    path('UpadateCartProductQuantity/<int:id>',views.UpadateCartProductQuantity.as_view(),name='UpadateCartProductQuantity'),
    path('UpadateBuyNowProductQuantityAll/<int:id>',views.UpadateBuyNowProductQuantityAll.as_view(),name='UpadateBuyNowProductQuantityAll'),
    
    
    
    path('BuyNowNew',views.BuyNowNew.as_view(),name="BuyNowNew"),
    path('PlaceOrderNew/<int:id>',views.PlaceOrderNew.as_view(),name="PlaceOrderNew"),
    path('PlaceOrderNew',views.PlaceOrderNew.as_view(),name="PlaceOrderNew"),

    path('SetDefaultAddressPlaceorder/<int:id>',views.SetDefaultAddressPlaceorder.as_view(),name="SetDefaultAddressPlaceorder"),

    path('UpadateBuyNowProductQuantity/<int:id>',views.UpadateBuyNowProductQuantity.as_view(),name='UpadateBuyNowProductQuantity'),

    path('AddToCart/<slug:slug>',views.AddToCartPage.as_view(),name="AddToCard"),
    path('AddToCart',views.AddToCartPage.as_view(),name="AddToCard"),
    path('TrendingMoviesAttire',views.TrendingMoviesAttire.as_view(),name="TrendingMoviesAttire"),
    path('Order/',views.Order.as_view(),name="Order"),
    path('CanceledProduct/<int:id>',views.CanceledProduct.as_view(),name="CanceledProduct"),
    path('Orderexchange',views.Orderexchange.as_view(),name="Orderexchange"),
    path('ReturnOrder/<int:id>',views.ReturnOrder.as_view(),name="ReturnOrder"),


    # path('add-to-card/<int:id>',views.AddToCard.as_view(),name="AddToCard"),
    # path('add-to-card',views.AddToCard.as_view(),name="AddToCard"),
    

    # Payment Method
    path('PaymenMethod/<int:id>',views.PaymenMethod.as_view(),name="PaymenMethod"),
    path('PaymenMethod',views.PaymenMethod.as_view(),name="PaymenMethod"),

    #Anushee code saveaddress
    path('remove_row/<int:id>',views.remove_row, name="remove_row"),
    path('remove_row_placeOrder/<int:id>',views.remove_row_placeOrder, name="remove_row_placeOrder"),

    #Place order new 
    path('EditAdressPlaceOrder/<int:id>',views.EditAdressPlaceOrder.as_view(),name="EditAdressPlaceOrder"),

    #ordersuccessfully 
    path('ordersuccessful',views.Ordersucessful.as_view(),name='ordersuccessful'),
    
    path('liked',views.LikeQuestionAnswer.as_view(), name='liked'),
    path('unliked',views.Un_LikeQuestionAnswer.as_view(), name='unliked'),


    path('SearchProduct',views.SearchProduct.as_view(), name='SearchProduct'),
    
    
    # rate
    path('Rate/<int:id> ',views.Rate.as_view(),name='Rate'),

    #sawan
    path('SeeAllPhotosVideos/<slug:slug>',views.SeeAllPhotosVideos.as_view(), name='SeeAllPhotosVideos'),
    
    path('filterdata/<slug:slug>',views.filterdata.as_view(), name='filterdata'),
#Anushree Code
    path('MenCategoryMobile/<slug:slug>',views.MenCategoryMobile.as_view(), name='MenCategoryMobile'),
    path('TopwearMobile/<slug:slug>',views.TopwearMobile.as_view(), name='TopwearMobile'),
    path('Faq',views.Faq.as_view(), name='Faq'),
    path('return-and-refund-policy',views.loadReturnRefundPolicy.as_view(), name='return-and-refund-policy'),
    path('privacy-policy',views.loadPrivacyPolicy.as_view(), name='privacy-policy'),
    path('term-and-conditions',views.loadTermAndConditions.as_view(), name='term-and-conditions'),
    path('become-supplier',views.loadBecomeSupplier.as_view(), name='become-supplier'),
    path('earn-scroly',views.loadEarnScroly.as_view(), name='earn-scroly'),
    path('see-all-reviews/<slug:slug>',views.loadSeeAllRevies.as_view(), name='see-all-reviews'),
    path('notification',views.loadNotification.as_view(), name='notification'),

    path('liked_review',views.LikeReview.as_view(), name='liked_review'),
    path('unliked_review',views.Un_LikeReview.as_view(), name='unliked_review'),



    path('Return_submit',views.Return_submit.as_view(),name="Return_submit"),


    # path('filter_data/<slug:slug>',views.filter_data.as_view(),name="filter_data"),
    path('about_us',views.aboutus,name='about_us'),


]

