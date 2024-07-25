from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name="home"),
    path('register',views.register,name='register'),
    path('logout',views.logout_page,name='logout'),
    path('login',views.login_page,name='login'),
    path('cart',views.cart_page,name='cart'),
    path('Favourite',views.fav_page,name='fav'),
    path('remove_cart/<str:cid>',views.remove_cart,name='removecart'),
    path('collections',views.collections,name='collections'),
    path('collections/<str:name>',views.collectionsviews,name='collections'),
    path('collections/<str:cname>/<str:pname>',views.product_details,name='product_details'),
    path('addtocart',views.add_to_cart,name="addtocart"),
]