"""crm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include 
#from django.http import HttpResponse # used to display things on our page
from django.conf import settings # lets us work with variables in settings.py
from django.conf.urls.static import static # will let us set the static files url pattern


# function for what happens in the home page
# passed in request because this function will 
# take in a request from user
#def home(request):
#    return HttpResponse('Home Page')
    
#def contact(request):
#    return HttpResponse("Contact Page")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')) # this says, instead of running a function, go to the aaccount (app)'s urls.py file and 
                                        # run the urlpatterns variable in there which will then run the functions in views.py

]

# allows us to view image files with links in web
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
