from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    homepage_view, register_view, login_view, logout_view, profile_view,
    product_list_view, product_detail_view, search_product_view,
    add_to_cart_view, view_cart_view, remove_from_cart_view, order_view, checkout_view, place_order_view
)

urlpatterns = [
   
    path('', homepage_view, name='home'),  
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),  

    # Product URLs
    path('products/', product_list_view, name='product_list'),
    path('details/<int:id>/', product_detail_view, name='product_detail'),
    path('search/', search_product_view, name='search'),

    # Cart URLs
    path('add_to_cart/<int:id>/', add_to_cart_view, name='add_to_cart'),  
    path('order/<int:id>/', order_view, name='order'),
    path('checkout/', checkout_view, name='checkout'),
    path('place_order/', place_order_view, name='place_order'),
    path('view_cart/', view_cart_view, name='view_cart'), 
    path('remove_from_cart/<int:id>/', remove_from_cart_view, name='remove_from_cart'), 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
