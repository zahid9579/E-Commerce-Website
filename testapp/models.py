from django.db import models
from django.contrib.auth.models import User  # Import Django's built-in User model


# Profile Model - Extending the built-in User model
class ProfileModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  
    phone = models.CharField(max_length=15)  
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username
    
    

# Category Model
class CategoryModel(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
    

# Product Model
class ProductModel(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.TextField()  
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE)  
    image = models.ImageField(upload_to="product_images/") 
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.title
    
    

# Cart Model
class CartModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to User
    product = models.ManyToManyField(ProductModel)  # Many-to-Many with Product
    quantity = models.IntegerField(default=1)  # Corrected spelling
    total_price = models.FloatField()
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart of {self.user.username}"
    
    

# Order Model
class OrderModel(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(ProductModel)  
    total_price = models.FloatField()
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
    
    
    

# Payment Model
class PaymentModel(models.Model):
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE)  
    payment_method = models.CharField(max_length=50)  # e.g., 'Credit Card', 'PayPal', 'Cash on delivery, etc.
    payment_status = models.CharField(max_length=20, choices=OrderModel.PAYMENT_STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Order {self.order.id}"
