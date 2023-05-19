from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.views import View
from . models import Product,Customer,Cart,OrderPlaced,Payment,Wishlist
from . models import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.conf import settings
import razorpay


# Create your views here.

def home(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
         totalitem = len(Cart.objects.filter(user=request.user))
         wishitem = len(Wishlist.objects.filter(user=request.user))
    #print("In view about function")
    return render(request,"home.html",locals())


def about(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
         totalitem = len(Cart.objects.filter(user=request.user))
         wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request,"about.html",locals())

def delete(request,rid):
    p=CustomerProfileForm.objects.get(id=rid)
    p.delete()
    return redirect('/address')

def contact(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
         totalitem = len(Cart.objects.filter(user=request.user))
         wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request,"contact.html",locals())


class CategoryView(View):
    def get(self,request,val):
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
         totalitem = len(Cart.objects.filter(user=request.user))
         wishitem = len(Wishlist.objects.filter(user=request.user))
        return render(request,"category.html",locals())

  
class CategoryTitle(View):
    def get(self,request,val):
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values('title')
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
         totalitem = len(Cart.objects.filter(user=request.user))
         wishitem = len(Wishlist.objects.filter(user=request.user))
        return render(request,"category.html",locals())

   
class ProductDetail(View):
    def get(self,request,pk):
        product = Product.objects.get(pk=pk)
        wishlist = Wishlist.objects.filter(Q(product=product) & Q(user=request.user))
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
         totalitem = len(Cart.objects.filter(user=request.user))
         wishitem = len(Wishlist.objects.filter(user=request.user))
        return render(request,"productdetail.html",locals())


class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegistrationForm()
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
         totalitem = len(Cart.objects.filter(user=request.user))
         wishitem = len(Wishlist.objects.filter(user=request.user))
        return render(request, 'customerregistration.html',locals())
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Congralutions! User Register Successfully.")
            return redirect("login")
        else:
            messages.warning(request,"Invalid Username and Password.")
            return render(request,'customerregistration.html',locals())

      
class ProfileView(View):
    def get(self,request):
        form=CustomerProfileForm()
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
         totalitem = len(Cart.objects.filter(user=request.user))
         wishitem = len(Wishlist.objects.filter(user=request.user))
        return render(request,'profile.html',locals())
    def post(self,request):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            mobile = form.cleaned_data['mobile']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            zipcode = form.cleaned_data['zipcode']
            state = form.cleaned_data['state']

            reg = Customer(user=user, name=name, mobile=mobile,
            locality=locality, city=city, zipcode=zipcode, state=state)
            reg.save()
            messages.success(request,"Congratulations! Profile Save Successfully!")
            return redirect ("address")
        else:
            messages.warning(request,"Invalid Input Data.")  
        return render(request,'profile.html',locals())


def address(request):
    add = Customer.objects.filter(user=request.user)
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
         totalitem = len(Cart.objects.filter(user=request.user))
         wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'address.html',locals()) 


class updateAddress(View):
    def get(self,request,pk):
        add =Customer.objects.get(pk=pk)
        form=CustomerProfileForm(instance=add)
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
         totalitem = len(Cart.objects.filter(user=request.user))
         wishitem = len(Wishlist.objects.filter(user=request.user))
        return render(request, 'updateAddress.html',locals()) 
    def post(self,request,pk):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.mobile = form.cleaned_data['mobile']
            add.locality = form.cleaned_data['locality'] 
            add.city = form.cleaned_data['city']
            add.zipcode = form.cleaned_data['zipcode']
            add.state = form.cleaned_data['state']
            add.save()
            messages.success(request,"Congratulations! Profile Save Successfully!")
        else:
            messages.warning(request,"Invalid Input Data")
        return redirect("address") 
        
'''
class PasswordResetConfirm():
    def post(request, uidb64, token):
        form = MySetPasswordForm(request.POST)
        return redirect("password_reset_complete")
''' 
def buy_now(request):
      user=request.user
      product_id = request.GET.get('prod_id')
      product = Product.objects.get(id=product_id)
      Cart(user=user,product=product).save()
      return redirect("/checkout")

def add_to_cart(request):  
      user=request.user
      product_id = request.GET.get('prod_id')
      product = Product.objects.get(id=product_id)
      Cart(user=user,product=product).save()
      return redirect("/cart")


def show_cart(request):
    user=request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
        totalamount = amount + 40
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
         totalitem = len(Cart.objects.filter(user=request.user))
         wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request,'addtocart.html',locals())


def show_wishlist(request):
    user=request.user
    cart = Cart.objects.filter(user=user)
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
         totalitem = len(Cart.objects.filter(user=request.user))
         wishitem = len(Wishlist.objects.filter(user=request.user))
    product = Wishlist.objects.filter(user=user)
    return render(request,'wishlist.html',locals())


class checkout(View):
    def get(self,request):
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
         totalitem = len(Cart.objects.filter(user=request.user))
         wishitem = len(Wishlist.objects.filter(user=request.user))
        user=request.user
        add=Customer.objects.filter(user=user)
        cart_items=Cart.objects.filter(user=user)
        famount = 0
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            famount = famount + value
        totalamount = famount + 40
        razoramount = int(totalamount * 100)
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        data = {"amount":razoramount, "currency":"INR","receipt":"order_rcptid_12"}
        payment_response = client.order.create(data=data)
        print(payment_response)
        order_id = payment_response['id']
        order_status = payment_response['status']
        if order_status == 'created':
            payment =  Payment(
               user=user,
               amount=totalamount,
               razorpay_order_id=order_id,
               razorpay_payment_status = order_status 
            )
            payment.save()
        return render(request,'checkout.html',locals())

   
def payment_done(request):
    order_id=request.GET.get('order_id')
    payment_id=request.GET.get('payment_id')
    cust_id=request.GET.get('cust_id')
    user=request.user
    customer=Customer.objects.get(id=cust_id)
    #To update payment status and payment id
    payment=Payment.objects.get(razorpay_order=order_id)
    payment.paid = True
    payment.razorpay_payment_id = payment_id
    payment.save()
    #To save order details
    cart=Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity,payment=payment).save()
        c.delete()
    return redirect("orders")


def orders(request):
    order_places=OrderPlaced.objects.filter(user=request.user) 
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
         totalitem = len(Cart.objects.filter(user=request.user))
         wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request,'orders.html',locals())


def plus_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        print(prod_id)
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)

  
def minus_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        #print(prod_id)
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)

  
def remove_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        #print(prod_id)
        data={
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)

 
def plus_wishlist(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        product=Product.objects.get(id=prod_id)
        user = request.user
        Wishlist(user=user,product=product).save()
        data={
            'message':'Wishlist Added Successfully',
        }
        return JsonResponse(data)
    

def minus_wishlist(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        product=Product.objects.get(id=prod_id)
        user = request.user
        Wishlist(user=user,product=product).delete()
        data={
            'message':'Wishlist Removed Successfully',
        }
        return JsonResponse(data)

   
def search(request):
    query = request.GET['search']
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
         totalitem = len(Cart.objects.filter(user=request.user))
         wishitem = len(Wishlist.objects.filter(user=request.user))
    product = Product.objects.filter(Q(title__icontains=query))
    return render(request,'search.html',locals())