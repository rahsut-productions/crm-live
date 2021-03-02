from django.contrib import admin

# Register your models here.

from .models import Customer, Product, Order, Tag # brings the Customer class from models.py that we created

admin.site.register(Customer) # registers Customer model (so can be used in Django administration page and more)
admin.site.register(Product)
admin.site.register(Tag)
admin.site.register(Order)