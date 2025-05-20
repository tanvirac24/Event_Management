from django.contrib.auth.models import User,Permission,Group
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm,PasswordResetForm,SetPasswordForm
from django.contrib.auth import authenticate,login,logout
from django import forms
import re
from django.contrib.auth import authenticate

class StyledFormMixin:
    def __init__(self,*arg,**kwarg):
        super().__init__(*arg,**kwarg)
        self.apply_styled_widgets()
    default_class="border px-4 py-2 border-black w-full my-2 focus:bg-gray-200"
    def apply_styled_widgets(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget,forms.TextInput):
                field.widget.attrs.update({
                    'class':self.default_class,
                    'placeholder': f"Enter {field.label}"}
                )
            elif isinstance(field.widget,forms.Textarea):
                field.widget.attrs.update({
                    'class': self.default_class,
                    'rows': '2',
                    'placeholder': f"Enter {field.label}"
                })
            elif isinstance(field.widget,forms.SelectDateWidget):
                field.widget.attrs.update({
                    'class': "border px-4 py-2 border-black my-2 focus:bg-gray-200",
                    
                })
            elif isinstance(field.widget,forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    'class':"space-y-2",
                    
                })
            elif isinstance(field.widget,forms.PasswordInput):
                field.widget.attrs.update({
                    'class':self.default_class,
                    'placeholder': f"Enter {field.label}"
                })
            elif isinstance(field.widget,forms.EmailInput):
                field.widget.attrs.update({
                    'class':self.default_class,
                    'placeholder': f"Enter {field.label}"
                })
            elif isinstance(field.widget,forms.Select):
                field.widget.attrs.update({
                    'class':self.default_class,
                    
                })
            elif isinstance(field.widget,forms.FileInput):
                field.widget.attrs.update({
                    'class':self.default_class,
                    
                })



class CustomLoginForm(StyledFormMixin,forms.Form):
    username = forms.CharField(widget=forms.TextInput)
    
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(self.request, username=username, password=password)
            if user is None:
                raise forms.ValidationError("Invalid username or password")
            self.user = user  # Store user to use in the view
        return cleaned_data

    def get_user(self):
        return getattr(self, 'user', None)

    

class CustomRegisterForm(StyledFormMixin,forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ['username']:
            self.fields[field].help_text = None



    password=forms.CharField(widget=forms.PasswordInput)
    confirm_password=forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model=User
        fields=['username','first_name','last_name','password','confirm_password','email']

    def clean_password(self):
        pas=self.cleaned_data.get('password')
        erors=[]
        if len(pas)<8:
            erors.append('Must contain 8 characters')
        if not re.search(r'[A-Z]',pas):
            erors.append('Must Contain one Uppercase Letter,Bro!')
        if not re.search(r'[a-z]',pas):
            erors.append('Must Contain one Lowercase Letter,Bro!')
        if not re.search(r'[0-9]',pas):
            erors.append('Must Contain one Digit,Bro!')
        if not re.search(r'[@#$%^&*]',pas):
            erors.append('Must Contain one Special Character,Bro!')
        if erors:
            raise forms.ValidationError(erors)
        return pas 

    def clean(self):
        cleaned_data=super().clean()
        pas=cleaned_data.get('password')
        confirmp=cleaned_data.get('confirm_password')

        if pas !=confirmp:
            raise forms.ValidationError('Password Doesnot Match')
        return cleaned_data
    
    def clean_email(self):
        email=self.cleaned_data.get('email')
        k=User.objects.filter(email=email).exists()
        if k:
            raise forms.ValidationError("Email Already Exist")
        return email
   
    
    
    # def save(self, commit=True):   #For hashing
    #     user = super().save(commit=False) #check-2
    #     user.set_password(self.cleaned_data['password']) 
    #     if commit:
    #         user.save()
    #     return user
""""----------------Pure LoginForm----------------"""
# class CustomLoginForm(forms.ModelForm):
    
#     def __init__(self, request,*args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field in ['username']:
#             self.fields[field].help_text = None
#     password=forms.CharField(widget=forms.PasswordInput(attrs={'class': 'border  px-4 py-2 w-full my-2 focus:bg-gray-200', 
#                                                'placeholder': 'Enter Passoword',
                                               
#                                                }))
#     class Meta:
#         model=User
#         fields=['username','password']
#         widgets={
#             'username': forms.TextInput(attrs={'class': 'border  px-4 py-2 w-full my-2 focus:bg-gray-200', 
#                                                'placeholder': 'Enter Username'
                                               
#                                                })}
#     def clean(self):
#         cleaned_data = super().clean()
#         name = cleaned_data.get('username')
#         password = cleaned_data.get('password')

#         if not User.objects.filter(username=name).exists():
#             raise forms.ValidationError("Invalid username")  

#         user = authenticate(username=name, password=password)

#         if user is None:
#             raise forms.ValidationError("Invalid password") 

#         return cleaned_data 
   
class CustomChangeForm(StyledFormMixin,PasswordChangeForm):
    def __init__(self,*args, **kwargs):
        
        super().__init__(*args, **kwargs)
       
    
    def clean_new_password1(self):
        pas=self.cleaned_data.get('new_password1')
        erors=[]
        if len(pas)<8:
            erors.append('Must contain 8 characters')
        if not re.search(r'[A-Z]',pas):
            erors.append('Must Contain one Uppercase Letter,Bro!')
        if not re.search(r'[a-z]',pas):
            erors.append('Must Contain one Lowercase Letter,Bro!')
        if not re.search(r'[0-9]',pas):
            erors.append('Must Contain one Digit,Bro!')
        if not re.search(r'[@#$%^&*]',pas):
            erors.append('Must Contain one Special Character,Bro!')
        if erors:
            raise forms.ValidationError(erors)
        return pas 
    def form_invalid(self, form):
        print("Form errors:", form.errors)
        return super().form_invalid(form)

"""-------------Mixin  Applied---------------------"""
class CustomPasswordResetForm(StyledFormMixin,PasswordResetForm):
    pass
        
class CustomPasswordResetConfirmForm(StyledFormMixin,SetPasswordForm):
    def __init__(self,*args, **kwargs):
        
        super().__init__(*args, **kwargs)

        

class EditProfileForm(StyledFormMixin,forms.ModelForm):
    bio=forms.CharField(required=False,widget=forms.Textarea)
    phone=forms.CharField(required=False,widget=forms.TextInput)
    profile_image=forms.ImageField(required=False)
    class Meta:
        model=User
        fields=['email','first_name','last_name']
        


    

    def __init__(self,*args,**kwargs):
        self.userprofile = kwargs.pop('userprofile', None)

        super().__init__(*args,**kwargs)

        if self.userprofile:
            self.fields['bio'].initial=self.userprofile.bio
            self.fields['phone'].initial=self.userprofile.phone
            self.fields['profile_image'].initial= self.userprofile.profile_image

    def save(self,commit=True):
        user=super().save(commit=False)
#userprofile zodi thake tobe save korbe
        if self.userprofile:
            self.userprofile.bio= self.cleaned_data.get('bio')
            self.userprofile.phone= self.cleaned_data.get('phone')
            self.userprofile.profile_image= self.cleaned_data.get('profile_image')
            
            if commit:
                self.userprofile.save()
        if commit:
            user.save()
        return user


    

        
        
