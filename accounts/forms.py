from django.forms import ModelForm # importing modelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
# we're importing this fro mthe user screen in admin page
from django.contrib.auth.models import User
# we can do .models because this file is in same place as the models.py file
from .models import * # getting all models from models.py

# a place where the customer can update account settings
class CustomerForm(ModelForm):
    class Meta:
        model = Customer # the model we are referring to
        fields = '__all__' # all the fields
        exclude = ['user'] # exclude being able to change user because that's admin only stuff


# we inherit from ModelForm
class OrderForm(ModelForm):
    class Meta:
        #two fields have to be created here
        # this says create a form with all the fields
        model = Order
        # if I only wanted to use one field:
        # fields = ['customer', 'product']
        fields = '__all__'

# this class inherits from UserCreationForm
class CreateUserForm(UserCreationForm):
    class Meta:
            model = User
            # this creates form with these fields
            # password1 is password and password2 is confirm password
            fields = ['username', 'email', 'password1', 'password2']