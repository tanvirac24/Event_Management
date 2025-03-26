from django.urls import path
from users.views import signUp,signIn,signOut,activate_user,admin_dashboard


urlpatterns = [
    path('sign_up/',signUp,name='signup'),
    path('sign_in/',signIn,name='signin'),
    path('sign_out/',signOut,name='signout'),
    path('admin_dash/',admin_dashboard,name='admin-dashboard'),
    path('activate/<int:user_id>/<str:token>/',activate_user,name='activate'),
]
