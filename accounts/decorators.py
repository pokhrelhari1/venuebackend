from django.http import HttpResponse
from django.shortcuts import redirect


# decorator for user athentication
def unauthenticated_user(view_function):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index') #if the user is authenticated redirect to index page
        else:
            return view_function(request, *args, **kwargs)     #if the user is unauthenticated redirect to view function that is login page
    return wrapper_function

#user permission for pages
def allow_user(allow_roles=[]):
     def decorator(view_function):
         def wrapper_function(request, *args, **kwargs):
             group =None
             if request.user.groups.exists():
                 group= request.user.groups.all()[0].name
             if group in allow_roles:
                 return view_function(request,*args, **kwargs)
             else:
                 return HttpResponse("You are not authorize")
            
             return wrapper_function
         return decorator
    

def admin_only(view_function):
        def wrapper_function(request, *args, **kwargs):
            group =None
            if request.user.groups.exists():
                group= request.user.groups.all()[0].name

            if group == 'customer':
                return redirect('index')
            
            if group == 'admin':
                return view_function(request, *args, **kwargs)

        return wrapper_function
