from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.shortcuts import get_object_or_404
import datetime
# Create your views here.
def Index(request):
    return render(request, 'index.html')

def user_home(request):
    fruits = PRODUCT.objects.all()
    return render(request, 'user_home.html', locals())
def About(request):
    return render(request, 'about.html')

def News(request):
    return render(request, 'news.html')

def Contact(request):
    return render(request, 'contact.html')

def NotFound(request):
    return render(request, '404.html')




def Shop(request):
    fruits = PRODUCT.objects.all()
    return render(request, 'shop.html', locals())

def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')


def login_page(request):
    return render(request, 'login.html')


def reg(request):
    if request.method == 'POST':
        # fname = request.POST.get('firstname')
        # lname = request.POST.get('lastname')
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone')
        address = request.POST.get('address')
        psw = request.POST.get('psw')
        pincode = request.POST.get('pincode')
        try:
            User.objects.get(username=email)
            return render(request, 'login.html')
        except User.DoesNotExist:
            user = User.objects.create(
                                       name=name,
                                       email=email,
                                       username=email,
                                       address=address,
                                       user_type=3,
                                       is_staff=0,
                                       is_superuser=0,
                                       phone_number=phone_number,
                                       pincode=pincode
                                       )
            user.set_password(psw)
            user.save()
            login(request, user)
            return redirect(Index)


    else:
        return redirect(login_page)

def login_view(request):
    if request.method=='POST':
        email = request.POST.get('email')
        psw = request.POST.get('psw')
        user = authenticate(username=email, password=psw)
        if user is not None:
            if user.is_staff == 1:
                if user.is_superuser == 1:
                    login(request, user)
                    return redirect(admin_dashboard)
                else:
                    pass
            else:
                login(request, user)
                return redirect(user_home)
        else:
            return redirect(login_page)
    else:
        return redirect(login_page)

def logout_view(request):
    logout(request)
    return redirect(Index)

def items(request):
    fruits = PRODUCT.objects.all()
    return render(request, 'items.html', locals())

def add_items(request):
    return render(request, 'add_items.html')

def new_items(request):
    if request.method == "POST":
        item_code = request.POST.get('item_code')
        item_name = request.POST.get('item_name')
        category = request.POST.get('category')
        image = request.FILES.get('image')
        price = request.POST.get('price')
        try:
            PRODUCT.objects.get(item_code=item_code)
            return render(request,'items.html')
        except PRODUCT.DoesNotExist:
            products = PRODUCT.objects.create(item_code=item_code,
                                             item_name=item_name,
                                             category=category,
                                             image=image,
                                             price=price

            )
            products.save()
            return redirect(items)
        else:
            return render(request, 'items.html')
    else:
        return redirect(items)

def update(request,id):
    details = PRODUCT.objects.filter(id=id)
    return render(request,'update.html', locals())

def update_item(request,id):
    if request.method == 'POST':
        item_code = request.POST.get('item_code')
        item_name = request.POST.get('item_name')
        price = request.POST.get('price')
        image = request.FILES.get('image')
        try:
            PRODUCT.objects.get(id=id)
            PRODUCT.objects.filter(id=id).update(item_code=item_code,
                                                 item_name=item_name,
                                                 price=price
                                                 )
            instance = get_object_or_404(PRODUCT, id=id)
            if image:
                instance.image = image
            instance.save()
            return redirect(items)
        except PRODUCT.DoesNotExist:
            return redirect(update_item,id)
    else:
        return redirect(items)

def delete_item(request,id):
    try:
        PRODUCT.objects.get(id=id)
        PRODUCT.objects.filter(id=id).delete()
        return redirect(items)
    except PRODUCT.DoesNotExist:
        return redirect(items)

def customers(request):
    user_details = User.objects.filter(user_type=3)
    return render(request, 'customers.html', locals())


# user module
def shipping_charge(user):
    cart_objects = CART.objects.filter(user=user.id)
    if not cart_objects:
        return 0

    item_count = sum(item.quantity for item in cart_objects)
    total_price = sum(item.total for item in cart_objects)

    if total_price > 1000 or item_count > 20:
        return 0
    elif item_count > 10:
        return 20
    else:
        return 50


def cart_item(request):
    user = User.objects.get(id=request.user.id)
    try:
        cart_object = CART.objects.filter(user=request.user.id)
        if cart_object:
            food_details = PRODUCT.objects.all()
            item_count = 0
            total_price = 0
            shipping = 0
            for i in cart_object:
                item_count = item_count + i.quantity
                total_price = total_price + i.total
            # if total_price > 1000:
            #     shipping = 0
            # else:
            #     if item_count > 20:
            #         shipping = 0
            #     elif item_count > 10:
            #         shipping = 20
            #     else:
            #         shipping = 50
            shipping = shipping_charge(user)
            print(shipping)
            grand_total = total_price + shipping
            return render(request, 'cart.html', locals())
        else:
            return render(request, 'cart.html', locals())
    except:
        return render(request, 'cart.html', locals())

def add_to_cart(request,id):
    try:
        CART.objects.get(item=id)
        user_cart = CART.objects.filter(item=id)
        fruit_item = PRODUCT.objects.filter(id=id)
        for i in fruit_item:
            price = i.price
        for i in user_cart:
            quantity = i.quantity

        quantity += 1
        total = price * quantity
        CART.objects.filter(item_id=id).update(quantity=quantity,
                                          total=total)

        return redirect(cart_item)
    except CART.DoesNotExist:
        prod = PRODUCT.objects.get(id=id)
        user = User.objects.get(id=request.user.id)
        fruit_details = PRODUCT.objects.filter(id=id)
        for i in fruit_details:
            price = i.price
        new_item = CART.objects.create(item=prod,
                                       user=user,
                                       quantity=1,
                                       total=price
                                       )
        new_item.save()
        # CART.objects.create()

        return redirect(cart_item)

def delete_cart_item(request,id):
    cart_items = CART.objects.filter(id=id)
    cart_items.delete()
    return redirect(cart_item)

def Checkout(request):
    user = User.objects.get(id=request.user.id)
    cart_objects = CART.objects.filter(user=request.user.id)
    fruits = PRODUCT.objects.all()
    try:
        DELIVERY_ADDRESS.objects.get(user=user)
        total_price = 0
        # if request.method == "POST":
        #     quantity = int(request.POST.get('item-quantity'))
        #     # print(quantity)
        #
        for i in cart_objects:
            for j in fruits:
                if i.item_id == j.id:
                    total_price = total_price + (j.price * i.quantity)
        update_add = DELIVERY_ADDRESS.objects.filter(user=request.user.id)
        shipping = shipping_charge(user)
        grand_total = shipping + total_price

        return render(request, 'checkout.html', locals())

    except DELIVERY_ADDRESS.DoesNotExist:
        delivery_details = DELIVERY_ADDRESS.objects.create(user=user,
                                                       name =user.name,
                                                       address=user.address,
                                                       pincode=user.pincode,
                                                       email=user.email,
                                                       phone_number=user.phone_number)
        delivery_details.save()
        return render(request,'checkout.html', locals())

    return render(request, 'checkout.html', locals())


def Invoice(request):
    user = User.objects.get(id=request.user.id)
    delivery_address = DELIVERY_ADDRESS.objects.filter(user=user)
    cartitem = CART.objects.filter(user=user)
    subtotal = 0
    quantity = 0
    shipping = shipping_charge(user)
    x = datetime.datetime.now()
    for i in cartitem:
        product_det = PRODUCT.objects.get(id=i.item_id)
        product = PRODUCT.objects.filter(id=i.item_id)
        new_order = ORDER.objects.create(item=product_det,
                                         user=user,
                                         order_date=x,
                                         quantity=i.quantity,
                                         total=i.total,
                                         status=1)
        new_order.save()
        subtotal = subtotal + i.total
        quantity = quantity + i.quantity

    grand_total = shipping + subtotal
    my_orders = ORDER.objects.filter(user=user, order_date=x)
    my_products = PRODUCT.objects.all()
    CART.objects.filter(user=user).delete()
    return render(request, 'invoice.html', locals())

def Offers(request):
    fruits = PRODUCT.objects.all()
    offer_details = OFFER.objects.all()
    return render(request, 'offers.html', locals())

def Add_offer(request):
    fruits = PRODUCT.objects.all()
    return render(request, 'add_offer.html', locals())

def offer_form(request,id):
    fruits = PRODUCT.objects.filter(id=id)
    return render(request, 'offer_form.html', locals())

def apply_offer(request,id):
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        percentage = request.POST.get('percentage')
        validity = request.POST.get('validity')
        description = request.POST.get('description')
        try:
            OFFER.objects.get(item_id=id)
            OFFER.objects.filter(item_id=id).update(quantity=quantity,
                                               percentage=percentage,
                                               validity=validity,
                                               description=description)

            return redirect(Offers)
        except PRODUCT.DoesNotExist:
            fruits = PRODUCT.objects.get(id=id)
            fruit_details = PRODUCT.objects.filter(id=id)
            offers = OFFER.objects.create(quantity=quantity,
                                                percentage=percentage,
                                                validity=validity,
                                                description=description,
                                                item=fruits
                                                  )
            offers.save()
        off = OFFER.objects.filter(item_id=id)
        prod = PRODUCT.objects.filter(id=id)
        for i in off:
            for j in prod:
                if i.item_id == j.id:
                    off_price = (j.price * i.quantity)
                    print(off_price)


    return redirect(Offers,locals())
