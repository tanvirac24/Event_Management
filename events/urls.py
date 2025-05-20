from django.urls import path
from django.http import HttpResponse
from events.views import dash,user_dash,list,details,search,add_ctg,add_event,update_event,delete_event,organizer_details,organizer_list,admin_dashboard,create_groups,groups,assign_role,organizer_dashboard,rsvp_event

urlpatterns = [
    path('dash/',dash,),
    path("homet/",user_dash,name='homet'),
    # path('list/',list,name='list'),
    path('list/',list.as_view(),name='list'),
    path('details/<int:event_id>/',details,name='details'),
    # path('add_event/',add_event,name='adde'),
    path('add_event/',add_event.as_view(),name='adde'),
    # path('signup/',add_person,name='person'),
    path('add_catagory/',add_ctg,name='catagories'),
    # path('update_event/<int:event_id>/',update_event,name='update'),
    path('update_event/<int:event_id>/',update_event.as_view(),name='update'),
    path('delete_event/<int:event_id>/',delete_event,name='delete'),
    path('search_event/',search,name='srh'),
    # path('organizer_event/<int:event_id>/',organizer_details,name='orz-details'),
    path('organizer_event/<int:event_id>/',organizer_details.as_view(),name='orz-details'),
    path('organizer_list/',organizer_list,name='orz-list'),
    path('rspv/<int:event_id>/',rsvp_event,name='rsvp'),
   
    path('admin_dash/',admin_dashboard,name='admin-dash'),
    path('organizer_dash/',organizer_dashboard,name='organizer-dash'),
    path('create_group/',create_groups,name='create-group'),
    path('group/',groups,name='group'),
    path('<int:user_id>/assign_role/',assign_role.as_view(),name='assign-role'),
    # path('<int:user_id>/assign_role/',assign_role,name='assign-role'),
    
    
    
   
]
