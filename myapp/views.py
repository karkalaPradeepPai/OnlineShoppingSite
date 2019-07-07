from django.shortcuts import render,redirect, get_object_or_404, reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponse
from .models import Category, Product, Client, Order
from .forms import OrderForm,InterestForm
from django.shortcuts import render
from django.utils import timezone
import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
lastlogin = 'Your last login was more than one hour ago'


def index(request):
        cat_list = Category.objects.all().order_by('id')[:10]
        if request.session.has_key('username'):
            lastlogin = request.session['last_login']
        else:
            lastlogin=''
        return render(request, 'myapp/index.html', {'cat_list': cat_list,'last_login':lastlogin})

def about(request):
        cookievalue = request.COOKIES.get('about_visits')
        if(cookievalue== None):
            response = render(request, 'myapp/about.html',{'about_visits':'1'})
            response.set_cookie('about_visits',1,5*60)
            return response
        else:
            cookievalue=int(cookievalue)+1
            response = render(request, 'myapp/about.html', {'about_visits': cookievalue})
            response.set_cookie('about_visits', cookievalue)
            return response

def detail(request,cat_no):
        cat_list = Category.objects.filter(id=cat_no)
        product_list = Product.objects.filter(category__id=cat_no)
        return render(request, 'myapp/detail.html', {'cat_list': cat_list,'product_list':product_list})

def products(request):
        prodlist = Product.objects.all().order_by('id')[:10]
        return render(request, 'myapp/products.html', {'prodlist': prodlist})

def place_order(request):
    if request.session.has_key('username'):
        msg = ''
        prodlist = Product.objects.all()
        if request.method == 'POST':
            form = OrderForm(request.POST)
            if form.is_valid():
                order = form.save(commit=False)
                if order.num_units <= order.product.stock:
                    order.save()
                    p = Product.objects.get(name=order.product.name)
                    p.stock = order.product.stock - order.num_units
                    p.save()
                    msg = 'Your order has been placed successfully.'
                else:
                    msg = 'We do not have sufficient stock to fill your order.'
                return render(request, 'myapp/orderresponse.html', {'msg': msg})
        else:
            form = OrderForm()
            return render(request, 'myapp/placeorder.html', {'form': form, 'prodlist': prodlist})
    else:
        return redirect('/myapp/login')

def productdetail(request, prod_id):
        proddetail = Product.objects.get(id=prod_id)
        if request.method == 'POST':
            form = InterestForm(request.POST)
            if form.is_valid():
                if form.cleaned_data['interested'] == 1:
                    proddetail.interested=proddetail.interested+form.cleaned_data['interested']
                    proddetail.save()
            return redirect('/myapp/')
        else:
            form = InterestForm()
            return render(request, 'myapp/productdetail.html', {'form': form, 'proddetail': proddetail})

def llogin(request):
    if request.session.has_key('username'):
        return redirect('../myapp/')
    else:
        return render(request, 'myapp/login.html')

def user_login(request):
    if request.method == 'POST':
         username = request.POST['username']
         password = request.POST['password']
         user = authenticate(username=username, password=password)
         if user:
             if user.is_active:
                 login(request,user)
                 now = datetime.datetime.now()
                 lastlogin = now.strftime("%m/%d/%Y, %H:%M:%S")
                 request.session['username']=username
                 if not request.session.has_key('last_login'):
                     lastlogin = 'Your last login was more than one hour ago'
                     request.session['last_login'] = lastlogin
                     print(lastlogin)
                     return redirect('../myapp/myorders')
                 else:
                    request.session['last_login']=lastlogin
                    request.session.set_expiry(3600)
                    print(lastlogin)
                    return redirect('../myapp/myorders')
             else:
                return HttpResponse('Your account is disabled.')
         else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'myapp/login.html')

def user_logout(request):
    if request.session.has_key('username'):
        del request.session['username']
        logout(request)

        #now = datetime.datetime.now()
        #lastlogin = now.strftime("%m/%d/%Y, %H:%M:%S")
        request.session['last_login'] = lastlogin
        return HttpResponseRedirect('../myapp/login')
    else:
        return HttpResponseRedirect('../myapp/login')

def myorders(request):
    if request.session.has_key('username'):
        username = request.session['username']
        myorderlist = Order.objects.filter(client__first_name=username)
        if myorderlist:
            return render(request, 'myapp/myorders.html', {'myorderlist': myorderlist})
        else:
            return render(request, 'myapp/myorders.html', {'myorderlist': myorderlist})
    else:
        return HttpResponseRedirect('../myapp/login')
        #This else part will display if the user hasn't placed any order
def register(request):
    return render(request,"myapp/register.html")

def user_register(request):
    if request.POST:
        data = request.POST.copy()
        firstname = data.get('firstname')
        lastname = data.get('lastname')
        username = data.get('username')
        password = data.get('password')
        confirmpassword = data.get('confirmpassword')
        shippingaddress = data.get('address')
        city = data.get('city')
        province = data.get('province')
        interestedin = data.getlist('checks[]')

        if firstname.replace(" ", "").isalpha() and lastname.replace(" ", "").isalpha():
            if password == confirmpassword:
                client = Client.objects.create(first_name=firstname, last_name=lastname, username=username, shipping_address=shippingaddress,
                    city=city, province=province)
                client.set_password(password)
                client.interested_in.set(interestedin)
                client.save()
                messages.success(request, 'Registered successfully')
                return redirect('../myapp/login')
            else:
                messages.error(request, 'Password and Confirm-password must be same')
                return redirect('../myapp/register')
        else:
            messages.error(request, 'First name and Last name must be not empty')
            return redirect('../myapp/register')
    else:
        return redirect('../myapp/register')
