
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from events.event_form import EventModelForm,CatagoryModelForm,AssignRoleForm,CreateGroupForm
from events.models import Event,Catagory
from datetime import date
from django.db.models import Q,Count
from django. contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.models import User,Permission,Group
from django.contrib.auth.decorators import login_required,user_passes_test,permission_required
# Create your views here.
def is_admin(user):
    return user.groups.filter(name='Admin').exists()

def is_organizer(user):
    return user.groups.filter(name='Organizer').exists()


def is_participent(user):
    return user.groups.filter(name='Participent').exists()


def dash(request):
  
   
    return render(request,"pages/dashboard.html")

@login_required
def rsvp_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

   
    if request.user in event.assigned_to.all():
        messages.warning(request, "You have already RSVP'd for this event.")
    else:
        event.assigned_to.add(request.user) 
        messages.success(request, f"You have successfully RSVP'd for {event.title}!")

    return redirect('list') 

@user_passes_test(is_participent,login_url='no-permission')
def user_dash(request):
    type=request.GET.get('type')
    events=Event.objects.all()
    person=User.objects.filter(groups__name="Participent")
    
    total_event=events.count()
    total_person=person.count()
    upcoming=events.filter(Q(due_date__gt=date.today())).count()
    past_events=events.filter(Q(due_date__lt=date.today())).count()
    running_events=events.filter(Q(due_date=date.today())).count()

    if type=='upcoming':
        events=events.filter(Q(due_date__gt=date.today()))
        typed='Upcoming Events'
    elif type=='ended':
        events=events.filter(due_date__lt=date.today())
        typed='Ended Events'
    elif type=='running':
        events=events.filter(Q(due_date=date.today()))
        typed='Running Events'
    else:
        typed='Total Events'
    
        

    context={
        "events":events,
        "person":person,
        "total_event":total_event,
        "total_person":total_person,
        "upcoming":upcoming,
        "past_events":past_events,
        "running_events":running_events,
        "typed":typed

    }

    return render(request,"pages/home.html",context)

@user_passes_test(is_participent,login_url='no-permission')
def details(request,event_id):
    event= get_object_or_404(Event,id=event_id)

    return render(request,"pages/details.html",{"event":event})

@user_passes_test(is_participent,login_url='no-permission')
def list(request):
    events=Event.objects.all()
    person=User.objects.filter(groups__name="Participant")
    
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










@login_required
@permission_required("events.add_event",login_url='no-permission')
def add_event(request):
    # person=persons.objects.all()
    catagories=Catagory.objects.all()
    form=EventModelForm()


    if request.method =="POST":
        form=EventModelForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()

            
            return render(request,'organizer/add_event.html',{"form":form,"message":"Event Created Successfully"})
        

    context={
        "form":form,
    }
    return render(request,"organizer/add_event.html",context)


@login_required
@permission_required("events.change_event",login_url='no-permission')
def update_event(request,event_id):
    events=Event.objects.get(id=event_id)
    
    form=EventModelForm(instance=events)


    if request.method =="POST":
        form=EventModelForm(request.POST,request.FILES,instance=events)
        if form.is_valid():
            form.save()

            
            return render(request,'organizer/add_event.html',{"form":form,"message":"Updated Successfully"})
        

    context={
        "form":form,
    }
    return render(request,"organizer/add_event.html",context)


@login_required
@permission_required("events.delete_event",login_url='no-permission')
def delete_event(request,event_id):
    
    if request.method =="POST":
        events=Event.objects.get(id=event_id)
        if not request.user.has_perm("events.delete_event"):  
            messages.error(request, "You do not have permission to delete this event.")
            return redirect('no-permission')
        events.delete()

        messages.success(request,"Event Deleted Successfully!")
        return redirect("orz-list")
    else:
        messages.error(request,"Something is Wrong Bro!")
        return redirect("list")
    
    



# def add_person(request):
#     form=PersonsModelForm()
#     if request.method =="POST":
#         form=PersonsModelForm(request.POST)
#         if form.is_valid():
#             form.save()
            
        
#             return render(request,'pages/signup.html',{"formi":form,"message":"Participant Registered Successfully"})
        

#     context={
#         "formi":form,
#     }
#     return render(request,"pages/signup.html",context)



@login_required
@permission_required("events.add_catagory",login_url='no-permission')
def add_ctg(request):
    form=CatagoryModelForm()
    if request.method =="POST":
        form=CatagoryModelForm(request.POST)
        if form.is_valid():
            form.save()
           
       
            return render(request,'organizer/add_catagory.html',{"formi":form,"message":"Catagory Added Successfully"})


        

    context={
        "formi":form,
    }
    return render(request,"organizer/add_catagory.html",context)


# def view_event(request):
#     events=Event.objects.all()
#     return render(request,'')


def search(request):
       
       query = request.GET.get('q') 
       if query:
            events = Event.objects.filter(title__icontains=query)  
       else:
            events = Event.objects.all() 
       context = {"events": events, 
                  "query": query}
       return render(request, "pages/list.html", context)

def main(request):
    
    return HttpResponse("Type /events/home/ to See Actual Site")



@user_passes_test(is_organizer,login_url='no-permission')
def organizer_dashboard(request):
   
    return render(request,"organizer/organizer_dash.html")


@login_required
@permission_required("events.change_eventdetail",login_url='no-permission')
def organizer_details(request,event_id):
    event= get_object_or_404(Event,id=event_id)
    status_choice=Event.STATUS_CHOICES
    if request.method=='POST':
        selected_status=request.POST.get('task_status')
        event.status=selected_status
        event.save()
        return redirect('orz-details',event_id)
    return render(request,"organizer/organizer_details.html",{"event":event,"status_choices":status_choice})


@login_required
@permission_required("events.delete_event",login_url='no-permission')   
def organizer_list(request):
    
    events=Event.objects.all()
    person=User.objects.filter(groups__name="Participant")
    
    
    total_person=person.count()
   

    context={
        "events":events,
        "person":person,
        
        "total_person":total_person,
        
    }
    return render(request,'organizer/organizer_list.html',context)









@user_passes_test(is_admin,login_url='no-permission')
def admin_dashboard(request):
    users=User.objects.all()
    return render(request,"admincenter/admin_dash.html",{"users":users})

@user_passes_test(is_admin,login_url='no-permission')
def create_groups(request):
    form= CreateGroupForm()
    if request.method=='POST':
        form=CreateGroupForm(request.POST)
        if form.is_valid():
            group=form.save()
            messages.success(request,f"Group {group.name} has been created successfully")
            return redirect('create-group')
    

    return render(request,"admincenter/create_group.html",{"form":form})
@user_passes_test(is_admin,login_url='no-permission')
def groups(request):
    group=Group.objects.all()
    return render(request,"admincenter/group.html",{"group":group})

@user_passes_test(is_admin,login_url='no-permission')
def assign_role(request,user_id):
    form=AssignRoleForm()
    user=User.objects.get(id=user_id)

    if request.method== 'POST':
        form=AssignRoleForm(request.POST)
        if form.is_valid():
            role=form.cleaned_data.get('role')
            user.groups.clear()
            user.groups.add(role)
            messages.success(request,f"User {user.username} has been assigned to the {role.name} role")
            return redirect('admin-dash')
    return render(request,'admincenter/assign_role.html',{"form":form})


