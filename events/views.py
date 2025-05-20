
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
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.base import ContextMixin
from django.views.generic import ListView,DetailView,UpdateView
from django.contrib.auth.views import LoginView

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



"""------------Converted Class Based-View----------------"""
deco=[user_passes_test(is_participent,login_url='no-permission')]
@method_decorator(deco,name="dispatch")
class list(ListView):
    model=Event
    context_object_name= 'events'
    template_name='pages/list.html'
    def get_queryset(self):
        queryset= Event.objects.all()
        return queryset
        





        

    

"""------------Converted Class Based-View----------------"""
update_decorator=[login_required,permission_required("events.change_event",login_url='no-permission')]
@method_decorator(update_decorator,name="dispatch")
class update_event(UpdateView):
    model=Event
    form_class=EventModelForm
    template_name="organizer/add_event.html"
    pk_url_kwarg='event_id'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"]=self.get_form()
        
        return context
        

    
    def post(self,request,event_id,*args,**kwargs):
        self.object=self.get_object()
        form=EventModelForm(request.POST,request.FILES,instance=self.object)
        
        if form.is_valid():
            form.save()
        messages.success(request,"Event added successfully")
        return redirect('update',event_id)



"""------------Converted Class Based-View----------------"""
class add_event(ContextMixin,LoginRequiredMixin,PermissionRequiredMixin,View):
    login_url="no_permission"
    permission_required='events.add_event'
    template_name="organizer/add_event.html"
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['form']=kwargs.get('form',EventModelForm())
        return context
    
    def get(self,request,*args,**kwargs):
    
       
        form=EventModelForm()
        context=self.get_context_data()
        return render(request,self.template_name,context)
    

    def post(self,request,*args,**kwargs):
        if request.method =="POST":
            form=EventModelForm(request.POST,request.FILES)
            if form.is_valid():
                form.save()
                context=self.get_context_data(form=form)
                messages.success(request,"Event Created Successfully")

                
                return render(request,self.template_name,context)
            
            
            
        

    


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




def search(request):
    if request.method =="POST":   
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



"""------------Converted Class Based-View----------------"""
organizer_deco=[login_required,permission_required("events.change_eventdetail",login_url='no-permission')]
@method_decorator(organizer_deco,name='dispatch')
class organizer_details(DetailView):
    model=Event
    template_name="organizer/organizer_details.html"
    context_object_name= 'event'
    pk_url_kwarg='event_id'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print("DEBUG STATUS_CHOICES:", Event.STATUS_CHOICES)
        context['status_choices'] = Event.STATUS_CHOICES
        
        return context
    def get_queryset(self):
        queryset= Event.objects.all()
        
        return queryset
    def post(self, request, *args, **kwargs):
        event=self.get_object()
        selected_status=request.POST.get('task_status')
        event.status=selected_status
        event.save()
        return redirect('orz-details',event.id)

     
    
    


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



"""------------Converted Class Based-View----------------"""
assign_decorator=[user_passes_test(is_admin,login_url='no-permission')]
@method_decorator(assign_decorator,name="dispatch")
class assign_role(View):
    assign_template='admincenter/assign_role.html'
    def get(self,request,user_id,*args,**kwargs):
        user=User.objects.get(id=user_id)
        form=AssignRoleForm()
        return render(request,self.assign_template,{"form":form,"user":user})
    
    def post(self,request,user_id,*args,**kwargs):
        
        if request.method== 'POST':
            user=User.objects.get(id=user_id)
            form=AssignRoleForm(request.POST)
            if form.is_valid():
                role=form.cleaned_data.get('role')
                user.groups.clear()
                user.groups.add(role)
                messages.success(request,f"User {user.username} has been assigned to the {role.name} role")
                return redirect('admin-dash')
        return render(request,self.assign_template,{"form":form,"user":user})





