from django.urls import path
from users.views import signUp,signIn,signOut,activate_user,admin_dashboard,EditProfileView,CustomPasswordResetConfirmView,CustomPassResetView,CustomLoginView,ProfileView,CustomPasswordChangeView
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView,PasswordChangeView
from django.contrib.auth.views import PasswordChangeDoneView  

urlpatterns = [
    path('sign_up/',signUp,name='signup'),
    path('sign_in/',signIn,name='signin'),
    # path('sign_in/',CustomLoginView.as_view(),name='signin'),
    path('profile/',ProfileView.as_view(),name='profile'),
    path('sign_out/',LogoutView.as_view(),name='signout'),
    path('password_change/',CustomPasswordChangeView.as_view(),name='password_change'),
    path('password_reset/',CustomPassResetView.as_view(),name='password_reset'),
    path('password_reset/confirm/<uidb64>/<token>',CustomPasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('password_Done/',PasswordChangeDoneView.as_view(template_name='registration/accounts/pass_changedone.html'),name='password_change_done'),
    # path('sign_out/',signOut,name='signout'),
    path('admin_dash/',admin_dashboard,name='admin-dashboard'),
    path('edit_profile/',EditProfileView.as_view(),name='edit_profile'),
    path('activate/<int:user_id>/<str:token>/',activate_user,name='activate'),
]
