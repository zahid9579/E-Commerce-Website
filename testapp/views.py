from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from testapp.models import ProductModel, CartModel, OrderModel


# User Authentication Starts here

def homepage_view(request):
    return render(request, 'testapp/homepage.html')


# Register view for new User
def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save new user
            return redirect('login')  # Redirect to login page after registration
    else:
        form = UserCreationForm()
    
    return render(request, "register.html", {"form": form})


# Login view
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to home page after login
    else:
        form = AuthenticationForm()
    
    return render(request, "login.html", {"form": form})


# Logout view
def logout_view(request):
    logout(request) 
    return redirect('/')  


# Profile view (Requires login)
@login_required
def profile_view(request):
    return render(request, "testapp/profile.html", {"user": request.user}) 


# Product view starts here

# Product list view
def product_list_view(request):
    products = ProductModel.objects.all()
    return render(request, 'testapp/product_list.html', {'products': products})

# Product detail view
def product_detail_view(request, id):
    product = get_object_or_404(ProductModel, pk=id)
    return render(request, 'testapp/product_details.html', {'product': product})

# Product search view
def search_product_view(request):
    query = request.GET.get('q', '')  # Get search query from request
    product = ProductModel.objects.filter(title__icontains=query)  # Filter products by title
    return render(request, 'testapp/search_results.html', {'product': product, 'query': query})



# # Add to Cart View
def add_to_cart_view(request, id):
    product = get_object_or_404(ProductModel, pk=id)
    cart, created = CartModel.objects.get_or_create(user=request.user)
    cart.products.add(product)  # Use `products` instead of `product`
    cart.save()
    return redirect('view_cart')



# Order View
def order_view(request, id):
    product = get_object_or_404(ProductModel, pk=id)
    order, created = OrderModel.objects.get_or_create(user=request.user)
    order.products.add(product)  # Use `products` instead of `product`
    order.save()
    return redirect('checkout')






# View Cart
def view_cart_view(request):
    cart = CartModel.objects.filter(user=request.user).first()  
    return render(request, 'testapp/view_cart.html', {'cart': cart})


# Remove from Cart
def remove_from_cart_view(request, id):
    cart = CartModel.objects.filter(user=request.user).first()
    product = get_object_or_404(ProductModel, pk=id)
    if cart and product in cart.products.all():
        cart.products.remove(product)  # Use `products`
        cart.save()
    return redirect('view_cart')




# # Checkout View
def checkout_view(request):
    order = OrderModel.objects.filter(user=request.user).first()
    if order:
        total_price = order.total_price  # Get total price from the order
        return render(request, 'testapp/checkout.html', {'order': order, 'total_price': total_price})
    
    return redirect('product_list')  # Redirect to product list if no order exists



# def place_order_view(request):
#     cart = CartModel.objects.filter(user=request.user).first()
    
#     if cart and cart.product.exists():
#         order, created = OrderModel.objects.get_or_create(user=request.user)
#         for product in cart.product.all():
#             order.products.add(product)
        
#         order.save()
#         cart.product.clear()  # Clear cart after placing order
        
#         return redirect('product_list')  # Redirect to product list after order is placed
    
#     return redirect('checkout')  # If cart is empty, stay on checkout page


def place_order_view(request):
    cart = CartModel.objects.filter(user=request.user).first()
    
    if cart and cart.products.exists():
        order, created = OrderModel.objects.get_or_create(user=request.user)
        for product in cart.products.all():
            order.products.add(product)
        
        order.save()
        cart.products.clear()  # Clear cart after placing order
        
        return redirect('product_list')
    
    return redirect('checkout')
