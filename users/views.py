from django.shortcuts import render,redirect,HttpResponse
from users.forms import CustomRegisterForm,CustomPasswordResetForm,CustomLoginForm,CustomChangeForm,CustomPasswordResetConfirmForm,EditProfileForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.views import LoginView,PasswordChangeView,PasswordResetView,PasswordResetConfirmView
from django.views.generic import TemplateView,UpdateView
from django.urls import reverse_lazy
from users.models import UserProfile
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


class CustomLoginView(LoginView):
    form_class=CustomLoginForm
    def get_success_url(self):
        next_url=self.request.GET.get('next')
        return next_url if next_url else super().get_success_url()

class CustomPasswordChangeView(PasswordChangeView):
    template_name='registration/accounts/pass_change.html'
    form_class=CustomChangeForm
    # success_url = reverse_lazy('password_change_done')

class CustomPassResetView(PasswordResetView):
    template_name='registration/reset_password.html'
    from_class=CustomPasswordResetForm
    success_url = reverse_lazy('signin')
     
    def form_valid(self, form):
        messages.success(
            self.request,'A Reset email sent. Please check your email'
        )
        return super().form_valid(form)
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name='registration/reset_password.html'
    from_class=CustomPasswordResetConfirmForm
    success_url = reverse_lazy('signin')

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context["protocol"]='http' if self.request.is_secure() else 'http'
        context['domain']=self.request.get_host()
        return context
     
    def form_valid(self, form):
        messages.success(
            self.request,'Password Reset Successfully!'
        )
        return super().form_valid(form)


class ProfileView(TemplateView):
    template_name='registration/accounts/profile.html'
    
    def get_context_data(self, **kwargs):

            context = super().get_context_data(**kwargs)
            user= self.request.user
            context["username"] = user.username
            context["email"]= user.email 
            context["name"]= user.first_name 
            context["bio"]= user.userprofile.bio 
            context["phone"]= user.userprofile.phone
            context["profile_image"]= user.userprofile.profile_image
            context["member_since"]= user.date_joined
            context["last_login"]= user.last_login
            return context
class EditProfileView(UpdateView):
    model=User
    form_class=EditProfileForm
    template_name='registration/accounts/update_profile.html'
    context_object_name='form'

    def get_object(self):
        return self.request.user
    
    def get_form_kwargs(self):
        kwargs=super().get_form_kwargs()
        kwargs['userprofile']=UserProfile.objects.get(user=self.request.user)
        return kwargs
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        user_profile=UserProfile.objects.get(user=self.request.user)
        context['form']=self.form_class(
            instance=self.object, userprofile=user_profile
        )
        return context
    def form_valid(self,form):
        form.save(commit=True)
        return redirect('profile')





@login_required
def signOut(request):
    if request.method=='POST':
        logout(request)
        return redirect('home')

def activate_user(request,user_id,token):
    try:
        user=User.objects.get(id=user_id)
        if default_token_generator.check_token(user,token):

            user.is_active=True
            user.save()
            return redirect('signin')
        else:
            return HttpResponse("Invalid Token or User Id")
    except User.DoesNotExist:
        return HttpResponse("User Not Found")
        

def admin_dashboard(request):
    return render(request,'registration/dashboard.html')


