from django.contrib import admin
from django.urls import path,include
from core.views import home,permit
from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", home,name='home'),
    path('events/', include("events.urls")),
    path('users/', include("users.urls")),
     path('wrong/',permit,name="no-permission")
    

]+debug_toolbar_urls()

urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

