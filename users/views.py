from django.shortcuts import render,redirect
from users.forms import CustomRegisterForm,CustomLoginForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required,user_passes_test
# Create your views here.

def is_admin(user):
    return user.groups.filter(name='Admin').exists()


def signUp(request):
    if request.method == 'GET':
        form=CustomRegisterForm()
    if request.method == 'POST':
        
        form=CustomRegisterForm(request.POST)
        if form.is_valid():
          user=form.save(commit=False)
          user.set_password(form.cleaned_data.get('password'))
          user.is_active=False
          user.save()
            
          messages.success(request,'A mail has been sent')
          return redirect('signin')

        
            
    return render(request,'registration/signup.html',{"form":form})

def signIn(request):
    form=CustomLoginForm()
    if request.method=='POST':
        name=request.POST.get('username')
        pas=request.POST.get('password')
        
        user=authenticate(request,username=name,password=pas)
        if user is not None:
            login(request,user)
            if user.is_superuser:
                return redirect('admin-dash')
            elif user.groups.filter(name="Organizer").exists():  
                return redirect('orz-list')
            elif user.groups.filter(name="Participant").exists():  
                return redirect('homet')
            else:
                return redirect('homet')  

            
        else:
            messages.success(request,"No user!")
            
    
        
             
    return render(request,'registration/login.html',{"form":form})
@login_required
def signOut(request):
    if request.method=='POST':
        logout(request)
        return redirect('home')

def activate_user(request,user_id,token):
    user=User.objects.get(id=user_id)
    if default_token_generator.check_token(user,token):

        user.is_active=True
        user.save()
        return redirect('signin')


def admin_dashboard(request):
    return render(request,'registration/dashboard.html')


    