from django.db import models
from django.contrib.auth.models import User

# models are python classes that inherit from django models and allow us to create classes that represent database tables

# Create your models here.

# for each customer registered in shop
class Customer(models.Model):
    # null set to true buecase we already have some custom  ers
    # models.CASCADE means that when we delete customer, we will delete the relationship too (id est, user or admin)
    # blank is for so customer can be created without user
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    # max_length is the maximum amount of characters that can be used
    # null is there  incase customer gives us no phone, email, or name. 
    # That way, no error code will occur.
    name = models.CharField(max_length=200, null=True) # customer name variable. Because it's str val, CharField() is in use 
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    # null set to true so previously created accounts will still be usable
    # you'll only be able to do this if static folder is NOT in accounts folder and if MEDIA_ROOT has been configured in settings.py
    profilePic = models.ImageField(default="profile1.png", null=True, blank=True)
    # auto_now_add allows us to automatically create when the customer was added to database without extra code
    date_created = models.DateTimeField(auto_now_add=True, null=True) # DateTimeField will take a screen shot of the time/date of when model was added to data base

    def __str__(self):
        return self.name # allows for name of person to show in Django administration under accounts/Customers


# the category
class Tag(models.Model):
    # max_length is the maximum amount of characters that can be used
    # null is there  incase customer gives us no phone, email, or name. 
    # That way, no error code will occur.
    name = models.CharField(max_length=200, null=True) # customer name variable. Because it's str val, CharField() is in use 

    def __str__(self):
        return self.name # allows for name of person to show in Django administration under accounts/Customers


# for each product in store
class Product(models.Model):
    # we want to specify if this is an indoor item
    # or an outdoor item
    CATEGORY = (
            ('Indoor', 'Indoor'),
            ('Out door', 'Out Door'),
    )


    name = models.CharField(max_length=200, null=True)
    # FloatField for float value
    price = models.FloatField(null=True)
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    # blank - it makes it so we don't need a description. Makes it not a required field 
    description = models.CharField(max_length=200, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    # Tag is put in to tell that we want relationship with Tag class
    # (ManyToMany is a kind of system used in CRMs like Amazon (though they have it more complicated))
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name # allows for name of person to show in Django administration under accounts/Customers



# for each order for products
class Order(models.Model):
    # this is a tuple. 
    STATUS = (
            ('Pending', 'Pending'),
            ('Out for delivery', 'Out for delivery'),
            ('Delivered', 'Delivered'),
            )

    # Customer is added as a parameter to tell that this passed in is the parent model
    # on_delete is if a customer is deleted, the customer's orderr will still stay in
    # database. (for good design, keep it in the database still.)
    customer =  models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)# customer will be who ordered the product
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)# customer will be who ordered the product
    # product customer wants
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    # if the item is delivered, in transit, etc.
    # choices is their so a drop down menu can be created for which status to pick in STATUS tuple
    status = models.CharField(max_length=200, null=True, choices=STATUS)

    note = models.CharField(max_length=1000, null=True)

    # put so the name of order will display on HTML pages when used (e.g. delete.html)
    def __str__(self):
        return self.product.name
    
