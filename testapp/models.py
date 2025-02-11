from django.db import models
from django.contrib.auth.models import User


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
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


# Product Model
class ProductModel(models.Model):
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
   
    description = models.TextField()
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="product_images/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# Cart Model (Tracks Individual Items in Cart)
class CartModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(ProductModel)  # Rename 'product' to 'products'
    created_at = models.DateTimeField(auto_now=True)

    def total_price(self):
        return sum(product.price for product in self.products.all())  # Calculate dynamically

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
    products = models.ManyToManyField(ProductModel)  # Ensure this exists
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_total_price(self):
        return sum(product.price for product in self.products.all())

    def save(self, *args, **kwargs):
        self.total_price = self.calculate_total_price()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"


# Order Items Model (To Track Each Product in an Order)
class OrderItemModel(models.Model):
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Stores price at the time of order

    def __str__(self):
        return f"Order {self.order.id} - {self.product.title}"


# Payment Model
class PaymentModel(models.Model):
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50)  # e.g., 'Credit Card', 'PayPal', 'Cash on Delivery'
    payment_status = models.CharField(max_length=20, choices=OrderModel.PAYMENT_STATUS_CHOICES, default='Pending')
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Added for better tracking
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Order {self.order.id}"
