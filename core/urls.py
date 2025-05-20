from django.urls import path
from core.views import permit

urlpatterns = [
   path("not_allowed/",permit,name="no-permission")
]
