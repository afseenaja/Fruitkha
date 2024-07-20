from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.shortcuts import get_object_or_404
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.
def Index(request):
    return render(request, 'index.html')

@login_required
def user_home(request):
    fruits = PRODUCT.objects.all()
    offer_details = OFFER.objects.all()
    count = NOTIFICATION.objects.filter(user_id=request.user, read=False).count()
    # offer_det = OFFER.objects.filter()
    for i in offer_details:
        off_date = i.validity
    format_date = off_date.strftime("%b %d %Y %H:%M:%S")
    return render(request, 'user_home.html', locals())
def About(request):
    count = NOTIFICATION.objects.filter(user_id=request.user, read=False).count()
    return render(request, 'about.html',locals())

def News(request):
    count = NOTIFICATION.objects.filter(user_id=request.user, read=False).count()
    return render(request, 'news.html',locals())

def Contact(request):
    count = NOTIFICATION.objects.filter(user_id=request.user, read=False).count()
    return render(request, 'contact.html',locals())

def enquiry(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        x = datetime.now()
        contact = CONTACT.objects.create(name=name,
                                         email=email,
                                         phone_number=phone_number,
                                         subject=subject,
                                         message=message,
                                         enquiry_time=x
                                         )
        contact.save()
        admin_message = "You have a new message from {uname}".format(uname=request.user.name)
        admin = User.objects.get(is_superuser=1)

        NOTIFICATION.objects.create(user=admin,
                                    text=admin_message,
                                    read=False,
                                    table_no=3)
        return redirect(Contact)


def NotFound(request):
    return render(request, '404.html')

def dealofthemonth(request):

    fruits = PRODUCT.objects.all()
    offer_details = OFFER.objects.all().order_by('-id')
    formatted_date = []
    actual_price = []
    for i in offer_details:
        off_date = i.validity
        format_date = off_date.strftime("%b %d %Y %H:%M:%S")
        formatted_date.append(format_date)
    for i in offer_details:
        for j in fruits:
            if i.item_id == j.id:
                price = i.quantity * j.price
                actual_price.append(price)
    return render(request, 'dealofthemonth.html', locals())


def Shop(request):
    count = NOTIFICATION.objects.filter(user_id=request.user, read=False).count()
    fruits = PRODUCT.objects.all()
    return render(request, 'shop.html', locals())




def login_page(request):
    return render(request, 'login.html')


def reg(request):
    if request.method == 'POST':
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
            admin_message = "New user {uname} has registered in your site. #{uid}".format(uid=request.user.id, uname=user.name)
            admin = User.objects.get(is_superuser=1)

            NOTIFICATION.objects.create(user=admin,
                                        text=admin_message,
                                        read=False,
                                        table_no=1)
            user_message = "Welcome {uname}, you are successfully registered".format(uname=user.name)
            NOTIFICATION.objects.create(user=request.user,
                                        text=user_message,
                                        read=False,
                                        table_no=1)
            return redirect(user_home)


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

def user_notification(request):
    notification = NOTIFICATION.objects.filter(user_id=request.user.id).order_by('-id')
    note = NOTIFICATION.objects.filter(user=request.user, read=False)
    for i in note:
        i.read = True
        i.save()

    return render(request, 'user_notification.html', locals())

# admin module

def admin_dashboard(request):
    count = NOTIFICATION.objects.filter(user_id=request.user, read=False).count()
    recent = ORDER.objects.all().order_by('-id')
    user_details = User.objects.filter(user_type=3)
    item = PRODUCT.objects.all()
    ucount = 0
    revenue = 0
    order_count = 0
    icount = 0
    for i in user_details:
        ucount += 1
    for i in recent:
        revenue = revenue + i.total
        order_count = order_count + 1
    for i in item:
        icount = icount + 1
    return render(request, 'admin_dashboard.html', locals())

def order_details(request):
    count = NOTIFICATION.objects.filter(user_id=request.user, read=False).count()
    user_details = User.objects.filter(user_type=3)
    new_orders = ORDER.objects.filter(status=1)
    pending_orders = ORDER.objects.filter(status=2)
    delivered_orders = ORDER.objects.filter(status=3)
    # for i in order_detail:
    #     for j in user_details:
    #         if i.user == j.id:
    #             fn = j.first_name
    item = PRODUCT.objects.all()
    return render(request, 'order_details.html', locals())

def accept(request, id):
    ORDER.objects.filter(id=id).update(status=2)
    return redirect(order_details)


def pending(request, id):
    ORDER.objects.filter(id=id).update(status=3)
    return redirect(order_details)


def cancel(request, id):
    ORDER.objects.filter(id=id).update(status=4)
    return redirect(order_details)

def notifications(request):
    notification = NOTIFICATION.objects.filter(user_id=4).order_by('-id')
    note = NOTIFICATION.objects.filter(user=request.user, read=False)
    for i in note:
        i.read = True
        i.save()


    return render(request, 'notifications.html', locals())






def messages(request):
    count = NOTIFICATION.objects.filter(user_id=request.user, read=False).count()
    message = CONTACT.objects.all().order_by('-id')
    return render(request, 'messages.html', locals())

def items(request):
    count = NOTIFICATION.objects.filter(user_id=request.user, read=False).count()
    fruits = PRODUCT.objects.all()
    return render(request, 'items.html', locals())

def add_items(request):
    count = NOTIFICATION.objects.filter(user_id=request.user, read=False).count()
    return render(request, 'add_items.html', locals())

def new_items(request):
    count = NOTIFICATION.objects.filter(user_id=request.user, read=False).count()
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
            for i in products:
                oid = i.id
            text = "New Item has been Added #{oid}".format(oid=oid)
            NOTIFICATION.objects.create(user=request.user,
                                        text=text,
                                        read=False)
            return redirect(items)
        else:
            return render(request, 'items.html',locals())
    else:
        return redirect(items)

def update(request,id):
    count = NOTIFICATION.objects.filter(user_id=request.user, read=False).count()
    details = PRODUCT.objects.filter(id=id)
    return render(request,'update.html', locals())

def update_item(request,id):
    count = NOTIFICATION.objects.filter(user_id=request.user, read=False).count()
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
            return redirect(items,locals())
        except PRODUCT.DoesNotExist:
            return redirect(update_item,id)
    else:
        return redirect(items,locals())

def delete_item(request,id):
    try:
        PRODUCT.objects.get(id=id)
        PRODUCT.objects.filter(id=id).delete()
        return redirect(items)
    except PRODUCT.DoesNotExist:
        return redirect(items)

def customers(request):
    count = NOTIFICATION.objects.filter(user_id=request.user, read=False).count()
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
    offers = OFFER.objects.all()

    try:
        cart_object = CART.objects.filter(user=request.user.id)
        if cart_object:
            food_details = PRODUCT.objects.all()
            item_count = 0
            total_price = 0
            shipping = 0
            price_list = []
            for i in cart_object:
                item_count = item_count + i.quantity
                total_price = total_price + i.total
            for i in cart_object:
                for j in food_details:
                    if i.item_id == j.id:
                        act_price = i.quantity * j.price
                        price_list.append(act_price)
            print(price_list)

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

        return redirect(Shop)

def delete_cart_item(request,id):
    cart_items = CART.objects.filter(id=id)
    cart_items.delete()
    return redirect(cart_item)

def Checkout(request):
    count = NOTIFICATION.objects.filter(user_id=request.user, read=False).count()
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
                    total_price = total_price + i.total
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
    x = datetime.now()
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
    for i in my_orders:
        oid = i.id
    admin_message = "New Order has been placed #{oid}".format(oid=oid)
    admin = User.objects.get(is_superuser=1)

    NOTIFICATION.objects.create(user=admin,
                                text=admin_message,
                                read=False,
                                table_no=2)
    user_message = "your order for {item_count} items has been successfully placed".format(item_count=quantity)
    NOTIFICATION.objects.create(user=request.user,
                                text=user_message,
                                read=False,
                                table_no=2)
    CART.objects.filter(user=user).delete()

    return render(request, 'invoice.html', locals())

def Offers(request):
    count = NOTIFICATION.objects.filter(user_id=request.user, read=False).count()
    fruits = PRODUCT.objects.all()
    offer_details = OFFER.objects.all()
    # x = datetime.now()
    # OFFER.objects.filter(validity=x).delete()
    current_time = timezone.now()

    # Retrieve expired offers for debugging
    expired_offers = OFFER.objects.filter(validity__lt=current_time)

    # Delete expired offers
    expired_offers.delete()
    return render(request, 'offers.html', locals())

def Add_offer(request):
    count = NOTIFICATION.objects.filter(user_id=request.user, read=False).count()
    fruits = PRODUCT.objects.all()
    return render(request, 'add_offer.html', locals())

def offer_form(request,id):
    count = NOTIFICATION.objects.filter(user_id=request.user, read=False).count()
    fruits = PRODUCT.objects.filter(id=id)
    return render(request, 'offer_form.html', locals())

def apply_offer(request,id):
    count = NOTIFICATION.objects.filter(user_id=request.user, read=False).count()
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))
        percentage = int(request.POST.get('percentage'))
        validity = request.POST.get('validity')

        description = request.POST.get('description')

        try:
            OFFER.objects.get(item_id=id)
            prod_details = PRODUCT.objects.filter(id=id)
            for i in prod_details:
                p = float(i.price)
            offer_price = ((p * quantity) - ((percentage / 100) * (p * quantity)))
            OFFER.objects.filter(item_id=id).update(quantity=quantity,
                                               percentage=percentage,
                                               validity=validity,
                                               description=description,
                                               offer_price=offer_price
                                                    )

            return redirect(Offers)
        except OFFER.DoesNotExist:
            fruits = PRODUCT.objects.get(id=id)
            fruit_details = PRODUCT.objects.filter(id=id)
            for i in fruit_details:
                p = float(i.price)
            offer_price = ((p * quantity) - ((percentage / 100) * (p * quantity)))

            offers = OFFER.objects.create(quantity=quantity,
                                                percentage=percentage,
                                                validity=validity,
                                                description=description,
                                                item=fruits,
                                                offer_price=offer_price
                                                  )
            offers.save()
            return redirect(Offers)
        off = OFFER.objects.filter(item_id=id)
        prod = PRODUCT.objects.filter(id=id)
    return redirect(Offers,locals())

def offer_cart(request,id):
    offers = OFFER.objects.get(item_id=id)

    try:
        CART.objects.get(item=id)
        CART.objects.filter(item_id=id).update(quantity=offers.quantity,
                                               total=offers.offer_price)

        return redirect(dealofthemonth)

    except CART.DoesNotExist:
        prod = PRODUCT.objects.get(id=id)
        user = User.objects.get(id=request.user.id)
        new_item = CART.objects.create(item=prod,
                                       user=user,
                                       quantity=offers.quantity,
                                       total=offers.offer_price
                                       )
        new_item.save()
    # CART.objects.create()
        return redirect(dealofthemonth)

    return redirect(dealofthemonth)


def profile(request):
    return render(request, 'profile.html')

def update_address(request):
    # user = User.objects.filter(id=request.user.id)
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        pincode = request.POST.get('pincode')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        try:
            User.objects.get(id=request.user.id)
            User.objects.filter(id=request.user.id).update(first_name=first_name,
                                                           last_name=last_name,
                                                           address=address,
                                                           pincode=pincode,
                                                           email=email,
                                                           phone_number=phone_number)
            return redirect(profile)
        except User.DoesNotExist:
            return redirect(profile)
    else:
        return redirect(profile)

def order_history(request):
    user_data = User.objects.filter(id=request.user.id)
    order_objects = ORDER.objects.filter(user_id=request.user.id).order_by('-order_date')
    product_details = PRODUCT.objects.all()
    orders_date_list = []
    total_list = []

    for i in order_objects:
        if i.order_date in orders_date_list:
            continue
        else:
            orders_date_list.append(i.order_date)

    # print(orders_date_list)
    total = 0
    for j in orders_date_list:
        total = 0
        for k in order_objects:

            if j == k.order_date:
                total += k.total
        total_list.append(total)
    # print(total_list)

    # print(orders_date)

    return render(request, 'order_history.html', locals())