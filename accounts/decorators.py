from django.http import HttpResponse
from django.shortcuts import redirect

# view func will be a function taken from another file
# will happen when @unauthenticatedUser is put in, the func under it will be viewFunc
def unauthenticatedUser(viewFunc):
    def wrapperFunc(request, *args, **kwargs):
        if request.user.is_authenticated: # if user put in right credentials to log in
            return redirect('home') # bring them to home page
        else:
            # run everything else in the original function
            return viewFunc(request, *args, **kwargs)
    
    return wrapperFunc

def allowedUsers(allowedRoles=[]):
    def decorator(viewFunc):
        def wrapperFunc(request, *args, **kwargs):
            group = None
            # exists is build in func
            if request.user.groups.exists():
                # group is set to the name of first group that user is apart of
                group = request.user.groups.all()[0].name

            # exempli gratia, if admin is an allowed group
            if group in allowedRoles:
                return viewFunc(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorised to view this page.')
        return wrapperFunc
    return decorator


# what's done in this function is a quick fix. You would not want to d  o this normally
def adminOnly(viewFunc):
    def wrapperFunc(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'customer':
            return redirect('user-page')
            
        if group == 'admin':
            # admin is allowed to be there
            return viewFunc(request, *args, **kwargs)

    return wrapperFunc