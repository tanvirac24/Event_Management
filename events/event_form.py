from django import forms
from django.http import HttpResponse
from events.models import Event,Catagory
from datetime import date
from users.forms import StyledFormMixin
from django.contrib.auth.models import User,Permission,Group








#Model Form
class EventModelForm(StyledFormMixin,forms.ModelForm):
    
    class Meta:
        model=Event
        fields=['title','description','status','location','due_date','catagory','asset']  #,'assigned_to'
        widgets={
            'due_date':forms.SelectDateWidget,


        }



class CatagoryModelForm(StyledFormMixin,forms.ModelForm):
    class Meta:
        model=Catagory
        fields=['name','description']
        
        
class AssignRoleForm(StyledFormMixin,forms.Form):
    role=forms.ModelChoiceField(
        queryset=Group.objects.all(),
        empty_label="Select a Role"
    #     widget=forms.Select(attrs={  
    #         'class': 'border px-4 py-2 w-full my-2 focus:bg-gray-200',
    #     })
    )

class CreateGroupForm(StyledFormMixin,forms.ModelForm):

    permissions=forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={  
            'class': 'border  p-2   focus:bg-gray-200',
        }),
        required=False,
        label='Assign Permission'
    )
    class Meta:
        model=Group
        fields=['name','permissions']
       