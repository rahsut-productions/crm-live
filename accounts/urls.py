from django.urls import path

# we do as auth_views because it seperates our views that we import below this import and this one
# this import is for password change 
from django.contrib.auth import views as auth_views

from . import views # 



urlpatterns = [
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    # name parameter is used so we can reference these in html files
    path('', views.home, name="home"),
    path('user/', views.userPage, name="user-page"),
    path('products/', views.products, name="products"), # when you go to the products page, we'll cause products function in views.py
    # what ever is put next to 'str:' has to be the same in the function.
    # since we put views.customer as the second parameter, pk has to be passed in
    # as a parameter in the customer function in views.py 
    # the str and the angle brackets are Django's way of letting us make this dynamic 
    path('customer/<str:pk>/', views.customer, name="customer"),
    path('create_order/<str:pk>/', views.createOrder, name="create_order"),
    path('update_order/<str:pk>/', views.updateOrder, name="update_order"),
    path('delete_order/<str:pk>/', views.deleteOrder, name="delete_order"),
    path('account/', views.accountSettings, name="account"),
    
    # for all the password ones; the name is specific, DO NOT use different name
    path('reset_password/', 
    auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"), 
    name="reset_password"),
    
    path('reset_password_sent/', 
    auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"),
     name="password_reset_done"),
    
    # uidb64 is the user's id encoded in base 64
    # token to check that the password is valid
    path('reset/<uidb64>/<token>',
     auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"),
     name="password_reset_confirm"),

    path('reset_password_complete/', 
    auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"),
     name="password_reset_complete")
]

'''
FOR PASSWORD CHANGE FORM (KEY TO HOW TO USE):

These views are classed based views; it is possible to customise. For more info, check
Django documentation.   

1 - Submit email form                           //PasswordResetView.as_view()
2 - Email sent success message                  //PasswordResetDoneView.as_view()
3 - Link to password Reset form in email        //PasswordResetConfirmView.as_view()
4 - Password successfully changed message       //PasswordResetCompleteView.as_view()
'''