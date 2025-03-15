
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from events.event_form import eventform,personform,catagoryform,EventModelForm,PersonsModelForm,CatagoryModelForm
from events.models import Event,persons,Catagory
from datetime import date
from django.db.models import Q,Count
from django. contrib import messages

# Create your views here.
def dash(request):
  
   
    return render(request,"pages/dashboard.html")


def home(request):
    type=request.GET.get('type')
    events=Event.objects.all()
    person=persons.objects.all()
    
    total_event=events.count()
    total_person=person.count()
    upcoming=events.filter(status="UPCOMING").count()
    past_events=events.filter(status="ENDED").count()
    running_events=events.filter(Q(status="RUNNING") |Q(due_date=date.today())).count()

    if type=='upcoming':
        events=events.filter(Q(due_date__gt=date.today()))
    elif type=='ended':
        events=events.filter(due_date__lt=date.today())
    elif type=='running':
        events=events.filter(Q(status="RUNNING") |Q(due_date=date.today()))

    context={
        "events":events,
        "person":person,
        "total_event":total_event,
        "total_person":total_person,
        "upcoming":upcoming,
        "past_events":past_events,
        "running_events":running_events

    }

    return render(request,"pages/home.html",context)

def details(request,event_id):
    event= get_object_or_404(Event,id=event_id)

    return render(request,"pages/details.html",{"event":event})

def list(request):
    events=Event.objects.all()
    person=persons.objects.all()
    
    total_event=events.count()
    total_person=person.count()
    upcoming=events.filter(status="UPCOMING").count()
    past_events=events.filter(status="ENDED").count()
    

    context={
        "events":events,
        "person":person,
        "total_event":total_event,
        "total_person":total_person,
        "upcoming":upcoming,
        "past_events":past_events

    }
    return render(request,"pages/list.html",context)


# def add_event(request):
#     person=persons.objects.all()
#     catagories=Catagory.objects.all()
#     form=eventform(person=person,catagories=catagories)


#     if request.method =="POST":
#         form=eventform(request.POST,person=person,catagories=catagories)
#         if form.is_valid():
#             data=form.cleaned_data
#             title=data.get('title')
#             description=data.get('description')
#             location=data.get('location')
#             due_date=data.get('due_date')
#             status=data.get('status')
#             assigned_to=data.get('assigned_to')
#             catagory=data.get('catagory')
#             alo=Catagory.objects.get(id=catagory)

#             event=Event.objects.create(title=title,catagory=alo,description=description,due_date=due_date,location=location,status=status)

#             #adding participants individually by reverse
#             for man_id in assigned_to:
#                 person=persons.objects.get(id=man_id)
#                 event.assigned_to.add(person)


#     context={
#         "form":form,
#     }
#     return render(request,"pages/add_event.html",context)


# def add_person(request):
#     form=personform()
#     if request.method =="POST":
#         form=personform(request.POST)
#         if form.is_valid():
#             data=form.cleaned_data
#             name=data.get('name')
#             email=data.get('email')
#             persons.objects.create(name=name,email=email)


        

#     context={
#         "formi":form,
#     }
#     return render(request,"pages/signup.html",context)




# def add_ctg(request):
#     form=catagoryform()
#     if request.method =="POST":
#         form=catagoryform(request.POST)
#         if form.is_valid():
#             data=form.cleaned_data
#             name=data.get('name')
#             description=data.get('description')
#             Catagory.objects.create(name=name,description=description)


        

#     context={
#         "formi":form,
#     }
#     return render(request,"pages/add_catagory.html",context)











def add_event(request):
    person=persons.objects.all()
    catagories=Catagory.objects.all()
    form=EventModelForm()


    if request.method =="POST":
        form=EventModelForm(request.POST)
        if form.is_valid():
            form.save()

            
            return render(request,'pages/add_event.html',{"form":form,"message":"Event Created Successfully"})
        

    context={
        "form":form,
    }
    return render(request,"pages/add_event.html",context)



def update_event(request,event_id):
    events=Event.objects.get(id=event_id)
    
    form=EventModelForm(instance=events)


    if request.method =="POST":
        form=EventModelForm(request.POST,instance=events)
        if form.is_valid():
            form.save()

            
            return render(request,'pages/add_event.html',{"form":form,"message":"Updated Successfully"})
        

    context={
        "form":form,
    }
    return render(request,"pages/add_event.html",context)



def delete_event(request,event_id):
    
    if request.method =="POST":
        events=Event.objects.get(id=event_id)
        events.delete()

        messages.success(request,"Event Deleted Successfully!")
        return redirect("list")
    else:
        messages.error(request,"Something is Wrong Bro!")
        return redirect("list")
    
    



def add_person(request):
    form=PersonsModelForm()
    if request.method =="POST":
        form=PersonsModelForm(request.POST)
        if form.is_valid():
            form.save()
            
        
            return render(request,'pages/signup.html',{"formi":form,"message":"Participant Registered Successfully"})
        

    context={
        "formi":form,
    }
    return render(request,"pages/signup.html",context)




def add_ctg(request):
    form=CatagoryModelForm()
    if request.method =="POST":
        form=CatagoryModelForm(request.POST)
        if form.is_valid():
            form.save()
           
       
            return render(request,'pages/add_catagory.html',{"formi":form,"message":"Catagory Added Successfully"})


        

    context={
        "formi":form,
    }
    return render(request,"pages/add_catagory.html",context)


def view_event(request):
    events=Event.objects.all()
    return render(request,'')


def search(request):
       
       query = request.GET.get('q') 
       if query:
            events = Event.objects.filter(title__icontains=query)  
       else:
            events = Event.objects.all() 
       context = {"events": events, 
                  "query": query}
       return render(request, "pages/list.html", context)