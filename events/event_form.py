from django import forms
from django.http import HttpResponse
from events.models import Event,persons,Catagory
from datetime import date


class eventform(forms.Form):
    title=forms.CharField(max_length=250,label='Title')
    description=forms.CharField(widget=forms.Textarea,label='Description')
    status=forms.CharField(max_length=15,label="STATUS")
    # status=forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=STATUS_CHOICES,label="STATUS")
    location=forms.CharField(max_length=350)
    due_date=forms.DateField(widget=forms.SelectDateWidget,label='Due Date')
    catagory = forms.ChoiceField(label="Category", choices=[])
    assigned_to=forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=[],label="PARCIPANTS")
    
    # assigned_to = forms.ModelChoiceField(
    #     queryset=persons.objects.all(),  # Fetch all persons from the database
    #     widget=forms.Select(),
    #     label="Participants"
    # )
    def __init__(self,*args,**kwargs):
        person=kwargs.pop("person",[])
        catagories = kwargs.pop("catagories", [])
        
        super().__init__(*args,**kwargs)
        self.fields['assigned_to'].choices=[(emp.id,emp.name) for emp in person]
        self.fields['catagory'].choices = [(catg.id, catg.name) for catg in catagories]

 

                    # def __init__(self,*args,**kwargs):
                  #     employees=kwargs.pop("persons",[])
              #widget=forms.Select(choices=FRUIT_CHOICES))
class personform(forms.Form):
    name=forms.CharField(max_length=100,label="Name")
    email=forms.EmailField()

class catagoryform(forms.Form):
    name=forms.CharField(max_length=50,label="Name")
    description=forms.CharField(widget=forms.Textarea,label='Description')





#Model Form
class EventModelForm(forms.ModelForm):
    class Meta:
        model=Event
        fields=['title','description','status','location','due_date','catagory','assigned_to']
        widgets={
            'title':forms.DateInput(attrs={
                'class':'border  px-4 py-2 w-full focus:bg-gray-200',
                'placeholder':'Enter Title',
                

            }),
            'due_date':forms.DateInput(attrs={
                'class':'border  px-4 py-2 w-full focus:bg-gray-200 my-2',
                'placeholder':'Year-Month-Date',
                
                

            }),
            # 'assigned_to':forms.CheckboxSelectMultiple,
            'description':forms.DateInput(attrs={
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
            'assigned_to': forms.CheckboxSelectMultiple(attrs={'class': 'mt-2 border px-2 py-2 grid grid-cols-4 gap-1'}),

        }
        

        

class PersonsModelForm(forms.ModelForm):
    class Meta:
        model=persons
        fields=['name','email']
        widgets={
            'name':forms.DateInput(attrs={
                'class':'border  px-4 py-2 w-full focus:bg-gray-200',
                'placeholder':'Enter Name',
                

            }),
            
            # 'assigned_to':forms.CheckboxSelectMultiple,
            'email':forms.DateInput(attrs={
                'class':'border  px-4 py-2 w-full focus:bg-gray-200 my-2',
                'placeholder':'Enter E-mail',
                

            }),
            

        }
        




class CatagoryModelForm(forms.ModelForm):
    class Meta:
        model=Catagory
        fields=['name','description']
        widgets={
            'name':forms.DateInput(attrs={
                'class':'border  px-4 py-2 w-full focus:bg-gray-200',
                'placeholder':'Enter Catagory Name',
                

            }),
           
            # 'assigned_to':forms.CheckboxSelectMultiple,
            'description':forms.DateInput(attrs={
                'class':'border  px-4 py-2 w-full focus:bg-gray-200 my-2',
                'placeholder':'Write Within 100 words!',
                'rows': '2'

            }),
            

        }
        
