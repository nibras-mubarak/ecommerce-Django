from django.shortcuts import render
from shopkart.form import CustomUserForm
from . models import *
from django.shortcuts import redirect, render
from http.client import HTTPResponse
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.http import JsonResponse
import json

def home(request):
    products=product.objects.filter(trending=1)
    return render(request, 'shop/home.html',{"products": products})

 
def add_to_cart(request):
    if request.headers.get('x-requested-with')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data=json.load(request)
            product_qty=data['product_qty']
            product_id=data['pid']
            #print(request.user.id)
            product_status=product.objects.get(id=product_id)
            if product_status:
                if cart.objects.filter(user=request.user,product_id=product_id):
                    return JsonResponse({'status':'product Already in cart'}, status=200)
                else:
                    if product_status.quantity>=product_qty:
                        cart.objects.create(user=request.user,product_id=product_id,product_qty=product_qty)
                        return JsonResponse({'status':'Product Added to cart successfully'}, status=200)
           
        else:
            return JsonResponse({'status':'Login to Addcart'}, status=200)

    else:
        return JsonResponse({'status':'Invalid Access'}, status=200)

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Logout Successfully")
        return redirect("/")
       


def login_page(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        form=CustomUserForm()
    if request.method=='POST':
        name=request.POST.get('username')
        pwd=request.POST.get('password')
        user=authenticate(request,username=name,password=pwd)
        if user is not None:
            login(request,user)
            messages.success(request,"Logged succesfully")
            return redirect("/")
        else:
            messages.error(request,"Invalid username or password")
            return redirect("/login")

    return render(request, "shop/login.html",{"form": form})

def register(request):
    form=CustomUserForm()
    if request.method=='POST':
        form=CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Registration success")
            return redirect('/login')
    return render(request, 'shop/register.html',{"form":form})

def collections(request):
    Cate  = category.objects.filter(status=0)
    return render(request,'shop/collections.html',{"category": Cate})
def collectionsviews(request, name):
    if(category.objects.filter(name=name, status=0)):
        products=product.objects.filter(category__name=name)
        return render(request, 'shop/products/index.html',{"product": products, "category_name": name})
    else:
       
        return redirect(request, "No such categories")
    
def product_details(request,cname,pname):
  if(category.objects.filter(name=cname,status=0)):
    if(product.objects.filter(name=pname,status=0)):
        products=product.objects.filter(name=pname, status=0).first()
        return render(request, "shop/products/product_details.html", {"products":products})
    else:
       messages.error(request,"No such product Found")
       return redirect("collections")
    


def cart_page(request):
     if request.user.is_authenticated:
         Cart=cart.objects.filter(user=request.user)
         return render(request, "shop/cart.html",{"Cart":Cart})
     else:
         return redirect("/")   
     

def remove_cart(request, cid):
    cartitem=cart.objects.get(id=cid)
    cartitem.delete()
    return redirect("/cart")


def fav_page(request):
    if request.headers.get('x-requested-with')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data=json.load(request)
            product_id=data['pid']
            product_status=product.objects.get(id=product_id)
            if product_status:
                if Favourite.objects.filter(user=request.user,product_id=product_id):
                    return JsonResponse({'status':'Product Already Added to Favourite'},200)
                else:
                    Favourite.objects.filter(user=request.user,product_id=product_id)
                    return JsonResponse({'status':'Product  Added to Favourite'},200)
            
           
        else:
            return JsonResponse({'status':'Login to Addfavourite'}, status=200)

    else:
        return JsonResponse({'status':'Invalid Access'}, status=200)
