# redirect is imported so we can redirect to other links
from django.shortcuts import render, redirect
from django.http import HttpResponse
# form sets are a way to create multiple forms into one form
from django.forms import inlineformset_factory
# importing a form field for making the registration and login screens
from django.contrib.auth.forms import UserCreationForm

# authenticate will authenticate user for us. login will login a user for us. logout will log out a user for us
from django.contrib.auth import authenticate, login, logout
# this is for flash messages
from django.contrib import messages
# this makes it so a login is required
from django.contrib.auth.decorators import login_required
# we get group model (seen in Admin page)
from django.contrib.auth.models import Group


from .models import * # import for models so we query the models from models.py 
# done so we can use OrderForm, CreateUserForm, CustomerForm from forms.py that we made
from .forms import OrderForm, CreateUserForm, CustomerForm
# import OrderFilter class created in filters.py
# we can do this because filters.py is in same directory as this file
from .filters import OrderFilter

from .decorators import unauthenticatedUser, allowedUsers, adminOnly

@unauthenticatedUser
def registerPage(request):
    # we are rendering the form
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save() # this creates the user
            # allows us to get username of user that was just created
            # next 3 lines add user to users group
            username = form.cleaned_data.get('username')
            
            
            

            # messages if for the one thing we imported
            messages.success(request, 'Account was created for ' + username)

            # redirects to login page after registering
            return redirect('login')

    context = {'form':form}
    return render(request, 'accounts/register.html', context)


# specifically called loginPage because calling it login messes with a reserved function, login()'
# viewFunc in decorators.py unauthenticatedUser function, is login page when you put @funcname above func
@unauthenticatedUser
def loginPage(request):
    if request.method == 'POST':
        # we get values for username and password from what was trying to be logged in with
        username = request.POST.get('username')
        password = request.POST.get('password')
        # it will try to authenticate user but aseeing if username and password authenticate with database
        user = authenticate(request, username=username, password=password)
        # if user was able to be authenticated
        if user is not None:
            login(request, user) # built in function
            # return is necessary otherwise redirect won't occur
            return redirect('home')
        else:
            # will show this message if wrong username or password/not authenticated
            messages.info(request, 'The username or password is incorrect.')

    context = {}
    return render(request, 'accounts/login.html', context)

def logoutUser(request):
    logout(request) # logout is built in
    return redirect('login')

@login_required(login_url='login') # login required is built in, the @ is needed
@adminOnly
# function for what happens in the home page
# passed in request because this function will 
# take in a request from user
def home(request):
    # for the next two lines; this is querying
    orders = Order.objects.all()
    customers = Customer.objects.all()
    # gives us total number of customers in system
    totalCustomers = customers.count()
    # gives us total number of orders in system
    totalOrders = orders.count()
    # find any order marked as delievered & pending
    # count() gives us the amount of delivered & pending
    # status is passed in because we need to tell django
    # what to filter by    
    delivered = orders.filter(status="Delivered").count()
    pending = orders.filter(status="Pending").count()
    # dictionary to be used in html templates
    context = {'orders':orders, 'customers':customers, 
    'totalOrders':totalOrders, 'delivered':delivered,
    'pending':pending}

    # we render the dashboard.html 
    return render(request, 'accounts/dashboard.html', context)

def userPage(request):
    # allows us to get all the customer's orders
    orders = request.user.customer.order_set.all()
    print('ORDERS:', orders)
    totalOrders = orders.count()
    delivered = orders.filter(status='Delivered').count() 
    pending = orders.filter(status='Pending').count() 


    context = {'orders':orders, 'totalOrders':totalOrders, 
    'delivered':delivered, 'pending':pending}
    return render(request, 'accounts/user.html', context)        

@login_required(login_url='login')
@allowedUsers(allowedRoles=['customer'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()

    context = {'form':form}
    return render(request, 'accounts/account_settings.html', context)



@login_required(login_url='login') # login required is built in, the @ is needed
@allowedUsers(allowedRoles=['admin'])
def products(request):
    # gets all products put into the system 
    products = Product.objects.all()
    # we render the products.html 
    # the third parameter is the passing in of the products var
    # whatever the third parameter with quotes is called is what will be 
    # used in templates (products.html)
    return render(request, 'accounts/products.html', {'products':products})


@login_required(login_url='login') # login required is built in, the @ is needed
@allowedUsers(allowedRoles=['admin'])
def customer(request, pk):
    # get customer id
    customer = Customer.objects.get(id=pk)
    # get the id passed in by customer (pk is not built in)
    # you have to use the same name as used in urls.py
    customer = Customer.objects.get(id=pk)

    # grabs all orders in system
    orders = customer.order_set.all()
    # gets number of all orders (orders is not built in var)
    orderCount = orders.count()

    # the filter for filtering in the search
    # first parameter is sending request data to view and second parameter is queryset and queryset will be all the orders
    myFilter = OrderFilter(request.GET, queryset=orders)
    # variable holds filtered data
    #.qs for queryset
    orders = myFilter.qs

    # allows us to use variabls in html files
    context = {'customer':customer, 'orders':orders, 'orderCount':orderCount, 'myFilter':myFilter}
    return render(request, 'accounts/customers.html', context)

@login_required(login_url='login') # login required is built in, the @ is needed
@allowedUsers(allowedRoles=['admin'])

def createOrder(request, pk):
    # fields are from models.py
    # parameters are parent model, child model, the third are fields we want to allow, and the fourth is extra fields we want to add (increasing amount of orders we can add)
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10)  
    # this gets customer id
    customer = Customer.objects.get(id=pk)
    
    # instance in form and set 'customer' to the variable customer
    #form = OrderForm(initial={'customer':customer})

    # because we through in parent, we can reference the model
    # first parameter is for so no previous orders get referenced into create_order screen
    # (remove first parameter to comprehend what I mean)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    # request is the request passed in this function
    if request.method == "POST":
       # pass in request if POST data
       # request.POST is passed in because this is POST data
       # because we through in parent, we can reference the model
       formset = OrderFormSet(request.POST, instance=customer)
       if formset.is_valid():
           formset.save()
           # redirects to home page
           return redirect('/')

    context = {'formset':formset}
    return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login') # login required is built in, the @ is needed
@allowedUsers(allowedRoles=['admin'])

def updateOrder(request, pk):
    order = Order.objects.get(id=pk)

    form = OrderForm(instance=order)
    if request.method == "POST":
        # pass in request if POST data
        # we throw in instance so it doesn't create
        # a new one
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            # redirects to home page
            return redirect('/')

    context = {'form':form}
    return render(request, 'accounts/order_form.html', context) 

@login_required(login_url='login') # login required is built in, the @ is needed
@allowedUsers(allowedRoles=['admin'])

def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)

    if request.method == "POST":
        order.delete()
        return redirect('/')

    context = {'item':order}
    return render(request, 'accounts/delete.html', context)