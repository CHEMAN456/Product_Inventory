from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required



# Create your views here.

def register_view(request):    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        
        if form.is_valid():
            
            user = form.save()
            messages.success(request,f'{user.username} Created Successfully')
            return redirect('users:login')
    else:
        form = UserCreationForm()
            
    return render(request,'users/register.html',{'form':form})  

def login_view(request):
    
    if request.method == 'POST':
        
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request,username = username,password = password)

        if user:
            login(request, user)
            if user.is_superuser:
                messages.success(request, f'Welcome Superuser {user.username}, login successful!')
            else:
                messages.success(request, f'Welcome {user.username}, login successful!')
            return redirect('inventory:home')
        
        else:
            messages.error(request,f'Invalid Login,Try Again!')
            return redirect('users:login')
        
    return render(request,'users/login.html')
    
def logout_view(request):
    
    if request.method == 'POST':
        logout(request)
        messages.success(request,'You have been logged out successfully')
        return redirect('inventory:index')
    
    return render(request,'users/logout.html')


    