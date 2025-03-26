from django import forms
from django.http import HttpResponse
from events.models import Event,Catagory
from datetime import date
from django.contrib.auth.models import User,Permission,Group


# class eventform(forms.Form):
#     title=forms.CharField(max_length=250,label='Title')
#     description=forms.CharField(widget=forms.Textarea,label='Description')
#     status=forms.CharField(max_length=15,label="STATUS")
#     # status=forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=STATUS_CHOICES,label="STATUS")
#     location=forms.CharField(max_length=350)
#     due_date=forms.DateField(widget=forms.SelectDateWidget,label='Due Date')
#     catagory = forms.ChoiceField(label="Category", choices=[])
#     assigned_to=forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=[],label="PARCIPANTS")
    
#     # assigned_to = forms.ModelChoiceField(
#     #     queryset=persons.objects.all(),  # Fetch all persons from the database
#     #     widget=forms.Select(),
#     #     label="Participants"
#     # )
#     def __init__(self,*args,**kwargs):
#         person=kwargs.pop("person",[])
#         catagories = kwargs.pop("catagories", [])
        
#         super().__init__(*args,**kwargs)
#         self.fields['assigned_to'].choices=[(emp.id,emp.name) for emp in person]
#         self.fields['catagory'].choices = [(catg.id, catg.name) for catg in catagories]

 

#                     # def __init__(self,*args,**kwargs):
#                   #     employees=kwargs.pop("persons",[])
#               #widget=forms.Select(choices=FRUIT_CHOICES))
# class personform(forms.Form):
#     name=forms.CharField(max_length=100,label="Name")
#     email=forms.EmailField()

# class catagoryform(forms.Form):
#     name=forms.CharField(max_length=50,label="Name")
#     description=forms.CharField(widget=forms.Textarea,label='Description')





#Model Form
class EventModelForm(forms.ModelForm):
    
    class Meta:
        model=Event
        fields=['title','description','status','location','due_date','catagory','asset']  #,'assigned_to'
        widgets={
            'title':forms.TextInput(attrs={
                'class':'border  px-4 py-2 w-full focus:bg-gray-200',
                'placeholder':'Enter Title',
                

            }),

                

            
            # 'assigned_to':forms.CheckboxSelectMultiple,
            'description':forms.TextInput(attrs={
                'class':'border  px-4 py-2 w-full focus:bg-gray-200 my-2',
                'placeholder':'Write Within 300 words!',
                'rows': '2'

            }),
            'status': forms.Select(attrs={'class': 'border  px-4 py-2 w-full my-2  focus:bg-gray-200'}),
            'location': forms.TextInput(attrs={'class': 'border  px-4 py-2 w-full my-2 focus:bg-gray-200', 
                                               'placeholder': 'Enter event location'}),
            'due_date': forms.DateInput(attrs={'class': 'border  px-4 py-2 w-full my-2 focus:bg-gray-200', 
                                               'type': 'date'}),
            'catagory': forms.Select(attrs={'class': 'border  px-4 py-2 w-full my-2 mb-4 focus:bg-gray-200'}),
            # 'assigned_to': forms.CheckboxSelectMultiple(attrs={'class': 'mt-2 border px-2 py-2 grid grid-cols-4 gap-1'}),
            'asset': forms.FileInput(attrs={
                'class': 'border-2 p-2 w-full  bg-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500',
                'accept': 'image/*', 
            }),
        }
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['assigned_to'].queryset = User.objects.filter(groups__name="Participent")
        

        

# class PersonsModelForm(forms.ModelForm):
#     class Meta:
#         model=
#         fields=['username','name','last_name','password','email',]
#         widgets={
#             'username':forms.DateInput(attrs={
#                 'class':'border  px-4 py-2 w-full focus:bg-gray-200',
#                 'placeholder':'Enter Username',
                

#             }),
#             'name':forms.DateInput(attrs={
#                 'class':'border  px-4 py-2 w-full focus:bg-gray-200',
#                 'placeholder':'Enter First Name',
                

#             }),
#             'last_name':forms.DateInput(attrs={
#                 'class':'border  px-4 py-2 w-full focus:bg-gray-200',
#                 'placeholder':'Enter Last Name',
                

#             }),
#             'password':forms.DateInput(attrs={
#                 'class':'border  px-4 py-2 w-full focus:bg-gray-200',
#                 'placeholder':'Enter Password',
#                 'type':'password'
                

#             }),
            
#             # 'assigned_to':forms.CheckboxSelectMultiple,
#             'email':forms.DateInput(attrs={
#                 'class':'border  px-4 py-2 w-full focus:bg-gray-200 my-2',
#                 'placeholder':'Enter E-mail',
                

#             }),
            

#         }
        




class CatagoryModelForm(forms.ModelForm):
    class Meta:
        model=Catagory
        fields=['name','description']
        widgets={
            'name':forms.TextInput(attrs={
                'class':'border  px-4 py-2 w-full focus:bg-gray-200',
                'placeholder':'Enter Catagory Name',
                

            }),
           
            # 'assigned_to':forms.CheckboxSelectMultiple,
            'description':forms.TextInput(attrs={
                'class':'border  px-4 py-2 w-full focus:bg-gray-200 my-2',
                'placeholder':'Write Within 100 words!',
                'rows': '2'

            }),
            

        }
        
class AssignRoleForm(forms.Form):
    role=forms.ModelChoiceField(
        queryset=Group.objects.all(),
        empty_label="Select a Role",
        widget=forms.Select(attrs={  
            'class': 'border px-4 py-2 w-full my-2 focus:bg-gray-200',
        })
    )

class CreateGroupForm(forms.ModelForm):

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
        widgets={
            'name':forms.TextInput(attrs={'class': 'border  px-4 py-2 w-full my-2 focus:bg-gray-200', 
                                               'placeholder': 'Enter Group Name'}),
        }