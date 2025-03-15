from django.urls import path
from events.views import dash,home,list,details,add_event,add_person,add_ctg,update_event,delete_event

urlpatterns = [
    path('dash/',dash,),
    path('home/',home,name='home'),
    path('list/',list,name='list'),
    path('details/<int:event_id>/',details,name='details'),
    path('add_event/',add_event,name='adde'),
    path('signup/',add_person,name='person'),
    path('add_catagory/',add_ctg,name='catagories'),
    path('update_event/<int:event_id>/',update_event,name='update'),
    path('delete_event/<int:event_id>/',delete_event,name='delete'),
    
   
]
