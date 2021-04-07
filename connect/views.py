from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import GenreField,Request,SectorField

User = get_user_model()

# Index Page Of Entire Application
def index_view(request):
    return render(request,'connect/index.html')


# About Page Of Application
def about_view(request):
    return render(request,'about.html')


# Returns the List of Available Sectors
def sector_list(request):
    sectors = SectorField.objects.all()
    data = {
        'sectors':sectors
    }
    return render(request,'connect/sector-list.html',context=data)


class DisplayRequest(LoginRequiredMixin,View):
    login_url = '/login/'
    # redirect_field_name = ''

    def get(self,request,id,*args,**kwargs):
        pass

    def post(self,request,*args,**kwargs):
        pass
