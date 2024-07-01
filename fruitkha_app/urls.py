
from django.urls import path
from . import views
urlpatterns = [
    path('', views.Index, name='home'),
    path('about/', views.About, name='about'),
    path('news/', views.News, name='news'),
    path('contact/', views.Contact, name='contact'),
    path('notfound/', views.NotFound, name='notfound'),
    path('cart/', views.cart_item, name='cart'),
    path('checkout/', views.Checkout, name='checkout'),
    path('shop/', views.Shop, name='shop'),
    path('loginpage/', views.login_page, name='login'),
    path('register/', views.reg, name='register'),
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout'),
    path('user_home/', views.user_home, name='user_home'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('items/', views.items, name='items'),
    path('add_items/', views.add_items, name='add_items'),
    path('new_items/', views.new_items, name='new_items'),
    path('update/<int:id>', views.update, name='update'),
    path('update_item/<int:id>', views.update_item, name='update_item'),
    path('delete_item/<int:id>', views.delete_item, name='delete_item'),
    path('customers/', views.customers, name='customers'),
    path('add_to_cart/<int:id>', views.add_to_cart, name='add_to_cart'),
    path('delete_cart_item/<int:id>', views.delete_cart_item, name='delete_cart_item'),
    path('invoice/', views.Invoice, name='invoice'),
    path('offers/', views.Offers, name='offers'),
    path('add_offer/', views.Add_offer, name='add_offer'),
    path('offer_form/<int:id>', views.offer_form, name='offer_form'),
    path('apply_offer/<int:id>', views.apply_offer, name='apply_offer')
]
