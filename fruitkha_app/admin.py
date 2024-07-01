from django.contrib import admin
from . models import *
# Register your models here.
admin.site.register(User)
admin.site.register(PRODUCT)
admin.site.register(CART)
admin.site.register(ORDER)
admin.site.register(DELIVERY_ADDRESS)
admin.site.register(OFFER)
