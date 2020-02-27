from django.shortcuts import render
from .models import Topmenu
from eva.models import UserProfile
# Create your views here.
def index(request):
    topmenu=Topmenu.objects.all()
    try:
        user = UserProfile.objects.all()
        count = user.count()
        context={
            'topmenu':topmenu,
            'count': count
        }
        return render(request, 'myaifront/index.html', context)
    except Exception as e:
        pass
        context={
            'topmenu':topmenu,
            'count': ''
        }
        return render(request, 'myaifront/index.html', context)
