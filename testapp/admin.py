from django.contrib import admin
from testapp.models import ProfileModel, CategoryModel, ProductModel, CartModel, OrderModel, PaymentModel


# Register your models here.
admin.site.register(ProfileModel)
admin.site.register(CategoryModel)
admin.site.register(ProductModel)
admin.site.register(CartModel)
admin.site.register(OrderModel)
admin.site.register(PaymentModel)


