from django.shortcuts import render, get_object_or_404,redirect
from django.views.generic import View
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed, JsonResponse
from django.core.exceptions import ValidationError,PermissionDenied
from django.contrib import messages

from .models import GenreField,Request,SectorField
from .forms import RequestForm
import json, datetime, pytz


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
            requests = Request.objects.filter(sector=sector,is_first_year_req = True,deleted=False,pending=True)
        else:
            requests = Request.objects.filter(sector=sector,is_first_year_req = False,deleted=False,pending=True)

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
    

    def post(self,request,id,*args,**kwargs):
        sector_id = int(request.POST.get('sector-id'))
        sector = get_object_or_404(SectorField,pk=sector_id)

        form = RequestForm(request.POST)
        if(form.is_valid()):
            pass 

        genre = request.POST.get('genre_list')
        subject = form.cleaned_data['subject']
        content = form.cleaned_data['content']
        deadline = form.cleaned_data['deadline']
        match_with_same_gender = request.POST.get("match_with_same_gender",None)

        # Custom Form Verification
        
        live = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))

        if not ((live.date()==deadline.date() and live.time()<deadline.time()) or(live.date()<deadline.date())):
            messages.error(request,'Deadline Must Be Higher than Current Time!')
            return redirect('connect:create-request',id=sector_id)
    
        is_first_year_req = False
        if(request.user.info.year == 1):
            is_first_year_req = True

        if(match_with_same_gender is None):
            match_with_same_gender = False
        else:
            match_with_same_gender = True

        req_obj = Request.objects.create(
            requester = request.user,
            sector = sector,
            genre = genre,
            subject = subject,
            content = content,
            match_with_same_gender = match_with_same_gender,
            deadline = deadline,
            is_first_year_req = is_first_year_req
        )
        messages.success(request,"Your Request is Created Sucessfully!")
        return redirect('connect:index')


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


# Deletes the Given Request
@login_required
def request_delete(request,id):
    req_obj = get_object_or_404(Request,pk=id)
    sector_id = req_obj.sector.id

    if(request.user != req_obj.requester):
        messages.error("Permission Denied!, You are Not Creater of Request.")
    else:
        req_obj.deleted = True
        req_obj.save()

    return redirect('connect:display-request',id=sector_id)


# Displays the Detailed View of Given Request
@login_required
def detailed_request_view(request,id):
    req_obj = get_object_or_404(Request,pk=id)

    if req_obj.deleted:
        raise PermissionDenied()

    if (request.user.info.year != 1):
        if (req_obj.is_first_year_req):
            raise PermissionDenied()

    if (request.user.info.year == 1):
        if not (req_obj.is_first_year_req):
            raise PermissionDenied()

    context = {
        'req_object':req_obj
    }
    return render(request,'connect/request-detail.html',context=context)

        

