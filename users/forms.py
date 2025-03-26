from django.contrib.auth.models import User,Permission,Group
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login,logout
from django import forms
import re

    

class CustomRegisterForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ['username']:
            self.fields[field].help_text = None



    password=forms.CharField(widget=forms.PasswordInput(attrs={'class': 'border  px-4 py-2 w-full my-2 focus:bg-gray-200', 
                                               'placeholder': 'Enter Passoword',
                                               
                                               }

    ))
    confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={'class': 'border  px-4 py-2 w-full my-2 focus:bg-gray-200', 
                                               'placeholder': 'Retype Password',
                                               
                                               
                                               }))
    class Meta:
        model=User
        fields=['username','first_name','last_name','password','confirm_password','email']
        widgets={
            'username': forms.TextInput(attrs={'class': 'border  px-4 py-2 w-full my-2 focus:bg-gray-200', 
                                               'placeholder': 'Enter Username'
                                               
                                               }),
            
            'first_name': forms.TextInput(attrs={'class': 'border  px-4 py-2 w-full my-2 focus:bg-gray-200', 
                                               'placeholder': 'Enter First Name'}),
            
            'last_name': forms.TextInput(attrs={'class': 'border  px-4 py-2 w-full my-2 focus:bg-gray-200', 
                                               'placeholder': 'Enter Last Name'}),
            
            
            'email': forms.TextInput(attrs={'class': 'border  px-4 py-2 w-full my-2 focus:bg-gray-200', 
                                               'placeholder': 'Enter E-mail Address'}),
            }
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

class CustomLoginForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ['username']:
            self.fields[field].help_text = None
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class': 'border  px-4 py-2 w-full my-2 focus:bg-gray-200', 
                                               'placeholder': 'Enter Passoword',
                                               
                                               }))
    class Meta:
        model=User
        fields=['username','password']
        widgets={
            'username': forms.TextInput(attrs={'class': 'border  px-4 py-2 w-full my-2 focus:bg-gray-200', 
                                               'placeholder': 'Enter Username'
                                               
                                               })}
    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if not User.objects.filter(username=name).exists():
            raise forms.ValidationError("Invalid username")  

        user = authenticate(username=name, password=password)

        if user is None:
            raise forms.ValidationError("Invalid password") 

        return cleaned_data 
   
    