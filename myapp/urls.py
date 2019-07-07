from django.urls import path
from myapp import views

app_name = 'myapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('products', views.products, name='products'),
    path('products/<prod_id>',views.productdetail,name='productdetail'),
    path('placeorder', views.place_order, name='placeorder'),
    path('login',views.llogin,name='login'),
    path('user_login',views.user_login,name='userlogin'),
    path('myorders',views.myorders,name='myorders'),
    path('logout',views.user_logout,name='userlogout'),
    path('register',views.register,name='userRegister'),
    path('user_register',views.user_register,name='userregister'),
    path('<cat_no>',views.detail,name='detail'),

    ]
