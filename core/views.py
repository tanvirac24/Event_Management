from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required,user_passes_test,permission_required
# Create your views here.


def home(request):
    return render(request,'Homes.html')

def permit(request):
    return render(request,'no_permission.html')
