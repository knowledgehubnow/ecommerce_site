from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.views import View
from .forms import CustomerRegisterationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

#pdf 
from io import BytesIO
from django.template.loader import get_template 
from xhtml2pdf import pisa

class ProductViews(View):
    def get(self,request):
        topwear = Product.objects.filter(category='TW')
        bottomwear = Product.objects.filter(category='BW')
        mobile = Product.objects.filter(category='M')
        laptop = Product.objects.filter(category='L')

        return render(request,'app/home.html',{
            'topwear' : topwear,
            'bottomwear' : bottomwear,
            'mobile' : mobile,
            'laptop' : laptop,
        })

def home(request):
 return render(request, 'app/home.html')

class ProductDetailViews(View):
    def get(self,request,pk):
        product = Product.objects.get(pk=pk)
        item_exist = False
        if request.user.is_authenticated:
            item_exist = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        return render(request, 'app/productdetail.html',{
            'product' : product,
            'item_exist' :item_exist,
        })

def add_to_cart(request):
    if request.user.is_authenticated:
        user = request.user
        product_id = request.GET.get('prod_id')
        product = Product.objects.get(id=product_id)
        Cart(user=user,product=product).save()
        return redirect('/cart')
    else:
        return redirect('login')
@login_required(login_url='login')
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        print(cart)
        amount = 0.0
        shiping_amount = 70.0
        total_amount = 0.0
        print(total_amount)
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        #print(cart_product)
        if cart_product:
            for p in cart_product:
                temp_amount = (p.quantity * p.product.discounted_price)
                amount += temp_amount
                total_amount = amount + shiping_amount
            return render(request,'app/addtocart.html',{
                'cart':cart,
                'total_amount':total_amount,
                'amount':amount,
            })
        else:
            return render(request,'app/empty.html')

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity +=1
        c.save()
        amount = 0.0
        shiping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        #print(cart_product)
        for p in cart_product:
            temp_amount = (p.quantity * p.product.discounted_price)
            amount += temp_amount
        data = {
            'quantity': c.quantity, 
            'amount': amount, 
            'total_amount':amount + shiping_amount,
        }
        return JsonResponse(data)
    
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -=1
        c.save()
        amount = 0.0
        shiping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        #print(cart_product)
        for p in cart_product:
            temp_amount = (p.quantity * p.product.discounted_price)
            amount += temp_amount
        data = {
            'quantity': c.quantity, 
            'amount': amount, 
            'total_amount':amount + shiping_amount,
        }
        return JsonResponse(data)

def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shiping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        #print(cart_product)
        for p in cart_product:
            temp_amount = (p.quantity * p.product.discounted_price)
            amount += temp_amount
        data = {
            'amount': amount, 
            'total_amount': amount + shiping_amount,
        }
        return JsonResponse(data)

def buy_now(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/buynow.html',{
        'add':add,
    })

@login_required(login_url='login')
def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html',{
        'add' : add,
        'active':'btn btn-primary',
        })

@login_required(login_url='login')
def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html',{
        'order_placed' : op,
    })

def mobile(request,data=None):
    if data == None:
        mobile = Product.objects.filter(category='M')
    elif data == 'redmi' or data == 'samsung':
        mobile = Product.objects.filter(category='M').filter(brand=data)
    elif data == 'below':
        mobile = Product.objects.filter(category='M').filter(discounted_price__lt=10000)
    elif data == 'above':
        mobile = Product.objects.filter(category='M').filter(discounted_price__gt=10000)
    return render(request, 'app/mobile.html',{
        'mobile' : mobile,
    })

def laptop(request,data=None):
    if data == None:
        laptop = Product.objects.filter(category='L')
    elif data == 'acer' or data == 'hp':
        laptop = Product.objects.filter(category='L').filter(brand=data)
    elif data == 'below':
        laptop = Product.objects.filter(category='L').filter(discounted_price__lt=10000)
    elif data == 'above':
        laptop = Product.objects.filter(category='L').filter(discounted_price__gt=10000)
    return render(request, 'app/laptop.html',{
        'laptop' : laptop,
    })
    
def topwear(request,data=None):
    if data == None:
        topwear = Product.objects.filter(category='TW')
    elif data == 'acer' or data == 'hp':
        topwear = Product.objects.filter(category='TW').filter(brand=data)
    elif data == 'below':
        topwear = Product.objects.filter(category='TW').filter(discounted_price__lt=500)
    elif data == 'above':
        topwear = Product.objects.filter(category='TW').filter(discounted_price__gt=500)
    return render(request, 'app/topwear.html',{
        'topwear' : topwear,
    })

def bottomwear(request,data=None):
    if data == None:
        bottomwear = Product.objects.filter(category='BW')
    elif data == 'acer' or data == 'hp':
        bottomwear = Product.objects.filter(category='BW').filter(brand=data)
    elif data == 'below':
        bottomwear = Product.objects.filter(category='BW').filter(discounted_price__lt=500)
    elif data == 'above':
        bottomwear = Product.objects.filter(category='BW').filter(discounted_price__gt=500)
    return render(request, 'app/bottomwear.html',{
        'bottomwear' : bottomwear,
    })

def login(request):
 return render(request, 'app/login.html')

class CustomerRegisterationView(View):
    def get(self,request):
        forms = CustomerRegisterationForm()
        return render(request, 'app/customerregistration.html',{
            'forms':forms,
        })

    def post(self,request):
        forms = CustomerRegisterationForm(request.POST)
        if forms.is_valid():
            messages.success(request,"You are Registered Successfully.")
            forms.save()
        return render(request, 'app/customerregistration.html',{
            'forms':forms,
        })

def checkout(request):
    if request.user.is_authenticated:
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_item = Cart.objects.filter(user=user)
        amount = 0.0
        shiping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        if cart_product:
            for p in cart_product:
                temp_amount = (p.quantity * p.product.discounted_price)
                amount += temp_amount
            total_amount = amount + shiping_amount
        return render(request, 'app/checkout.html',{
            'add':add,
            'total_amount':total_amount,
            'cart_item':cart_item,
        })
    else:
        return redirect('login')
        
@login_required(login_url='login')
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)

    for c in cart:
        OrderPlaced(user=user,customer=customer,product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect('invoice',id=custid)

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html',{
            'form' : form,
            'active':'btn btn-primary',
        })
    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            city = form.cleaned_data['city']
            locality = form.cleaned_data['locality']
            zipcode = form.cleaned_data['zipcode']
            state = form.cleaned_data['state']

            data = Customer(user=usr,name=name, city=city, locality=locality, zipcode=zipcode, state=state)
            data.save()
            messages.success(request,"Congratulations!! Your Profile Successfully Updated")
        return render(request, 'app/profile.html',{
            'form' : form,
            'active':'btn btn-primary',
        })

def render_to_pdf(template_src,context_dict={}):
    template = get_template(template_src)
    html= template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1"),result))

    if not pdf.err:
        return result.getvalue()
    return None

    