from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed, JsonResponse

from .models import GenreField,Request,SectorField
from .forms import RequestForm
import json

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
    """
    Displays the Create Request Button with Recent Requests in Particular Sector
    """
    def get(self,request,id,*args,**kwargs):
        sector = get_object_or_404(SectorField,pk=id)

        if request.user.info.year == 1:
            requests = Request.objects.filter(sector=sector,is_first_year_req = True)
        else:
            requests = Request.objects.filter(sector=sector)

        data = {
            'sector':sector,
            'requests':requests,
        }
        return render(request,'connect/sector-detail.html',context=data)


class CreateRequest(LoginRequiredMixin,View):
    """
    Returns the Create-Request Form and After Submission, Saves the Data in db
    """
    def get(self,request,id,*args,**kwargs):
        sector = get_object_or_404(SectorField,pk=id) 
        form = RequestForm(initial={'sector':sector})
        data = {
            'form':form,
            'sector':sector,
        }
        return render(request,'connect/request-create.html',context=data)
    
    def post(self,request,*args,**kwargs):
        print(request.POST)



# Returns the Genere List for Particular Sector
@login_required
def genre_list_api(request):
    if request.method == 'POST':
        data_ =  json.loads(request.body)
        sector_id = data_.get('sector_id')

        sector = get_object_or_404(SectorField,pk=sector_id)

        data = {"sector-list":list()}
        genre_list = sector.genre.all()

        for i in genre_list:
            data['sector-list'].append(i.genre_type)
        return JsonResponse(data=data)
    return HttpResponseNotAllowed('GET')

        

