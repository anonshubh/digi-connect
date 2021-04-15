from django.shortcuts import render, get_object_or_404,redirect
from django.views.generic import View
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed, JsonResponse
from django.core.exceptions import ValidationError,PermissionDenied
from django.contrib import messages

from .models import GenreField,Request,SectorField,InitialMatchingRequest,FinalMatchingRequest
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
    def get(self,request,id,type_,*args,**kwargs):
        sector = get_object_or_404(SectorField,pk=id)
        
        if request.user.info.year == 1:
            requests_ = Request.objects.filter(sector=sector,is_first_year_req = True,deleted=False,pending=True)
        else:
            requests_ = Request.objects.filter(sector=sector,is_first_year_req = False,deleted=False,pending=True)
        
        final_requests =  []
        for i in requests_:
            if(i.match_with_same_gender):
                if(request.user.info.gender == i.requester.info.gender):
                    final_requests.append(i)
            elif(type_ == 1):
                if(request.user.info.gender == i.requester.info.gender):
                    final_requests.append(i)
            else:
                final_requests.append(i)


        data = {
            'sector':sector,
            'requests':final_requests,
            'type_':type_,
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

    return redirect('connect:display-request',id=sector_id,type_=0)


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
    
    if(req_obj.match_with_same_gender):
        if(request.user.info.gender != req_obj.requester.info.gender):
            raise PermissionDenied()
    
    already_sent = False
    initial_req_obj,created = InitialMatchingRequest.objects.get_or_create(request=req_obj)
    req_users = initial_req_obj.req_users.all()

    final_accepted = False
    final_req_obj,created1 = FinalMatchingRequest.objects.get_or_create(request=req_obj)
    final_req_users = final_req_obj.final_req_users.all()

    if(request.user in req_users):
        already_sent = True
    
    if(request.user in final_req_users):
        final_accepted = True

    context = {
        'req_object':req_obj,
        'already_sent':already_sent,
        'final_accepted':final_accepted
    }
    return render(request,'connect/request-detail.html',context=context)


# Adds New Requester to the Particular Request
@login_required
def add_or_remove_sender_view(request,id):
    req_obj = get_object_or_404(Request,pk=id)
    deadline = req_obj.deadline

    if req_obj.deleted:
        raise PermissionDenied()
    
    if (request.user == req_obj.requester):
        raise PermissionDenied()

    if (request.user.info.year != 1):
        if (req_obj.is_first_year_req):
            raise PermissionDenied()

    if (request.user.info.year == 1):
        if not (req_obj.is_first_year_req):
            raise PermissionDenied()
    
    if(req_obj.match_with_same_gender):
        if(request.user.info.gender != req_obj.requester.info.gender):
            raise PermissionDenied()

    live = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))

    if not ((live.date()==deadline.date() and live.time()<deadline.time()) or(live.date()<deadline.date())):
        messages.error(request,'Deadline Exceeded!')
        req_obj.deleted = True
        req_obj.save()
        return redirect('connect:detail-request',id=req_obj.id)
    
    initial_req_obj,created = InitialMatchingRequest.objects.get_or_create(request=req_obj)
    req_users = initial_req_obj.req_users.all()

    if(request.user in req_users):
        initial_req_obj.req_users.remove(request.user)
        messages.info(request,"Request Cancelled!")
    else:
        initial_req_obj.req_users.add(request.user)
        messages.success(request,"Request Sent Sucessfully!")
    
    return redirect('connect:detail-request',id=req_obj.id)
    

# Displays the List of Users Sent the Request for Particular Request
@login_required
def list_senders_in_request_view(request,id):
    req_obj = get_object_or_404(Request,pk=id)

    deadline = req_obj.deadline

    if req_obj.deleted:
        raise PermissionDenied()
    
    if (request.user.info.year != 1):
        if (req_obj.is_first_year_req):
            raise PermissionDenied()
    
    if (request.user != req_obj.requester):
        raise PermissionDenied()

    if (request.user.info.year == 1):
        if not (req_obj.is_first_year_req):
            raise PermissionDenied()
    
    if(req_obj.match_with_same_gender):
        if(request.user.info.gender != req_obj.requester.info.gender):
            raise PermissionDenied()

    live = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))

    if not ((live.date()==deadline.date() and live.time()<deadline.time()) or(live.date()<deadline.date())):
        messages.error(request,'Deadline Exceeded!')
        req_obj.deleted = True
        req_obj.save()
        return redirect('connect:detail-request',id=req_obj.id)
    
    initial_req_obj,created = InitialMatchingRequest.objects.get_or_create(request=req_obj)
    req_users = initial_req_obj.req_users.all()

    final_req_obj,created1 = FinalMatchingRequest.objects.get_or_create(request=req_obj)
    final_req_users = final_req_obj.final_req_users.all()

    accepted_back = {}

    for i in req_users:
        if(i in final_req_users):
            accepted_back[i] = 1
        else:
            accepted_back[i] = 0

    context = {
        'req_obj':req_obj,
        'req_users':req_users,
        'accepted_back':accepted_back
    }

    return render(request,'connect/requesting-list.html',context=context)


# Final Accept or Deny of Sender's Request
@login_required
def final_accept_view(request,id,username):
    user_obj = get_object_or_404(User,username=username)

    req_obj = get_object_or_404(Request,pk=id)
    deadline = req_obj.deadline

    if req_obj.deleted:
        raise PermissionDenied()

    if (request.user.info.year != 1):
        if (req_obj.is_first_year_req):
            raise PermissionDenied()

    if (request.user.info.year == 1):
        if not (req_obj.is_first_year_req):
            raise PermissionDenied()
    
    if(req_obj.match_with_same_gender):
        if(request.user.info.gender != req_obj.requester.info.gender):
            raise PermissionDenied()
    
    live = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))

    if not ((live.date()==deadline.date() and live.time()<deadline.time()) or(live.date()<deadline.date())):
        messages.error(request,'Deadline Exceeded!')
        req_obj.deleted = True
        req_obj.save()
        return redirect('connect:detail-request',id=req_obj.id)

    initial_req_obj,created = InitialMatchingRequest.objects.get_or_create(request=req_obj)
    req_users = initial_req_obj.req_users.all()
    if not (user_obj in req_users):
        messages.error(request,"Initial User Not Matched!")
        raise PermissionDenied()
    
    final_req_obj,created1 = FinalMatchingRequest.objects.get_or_create(request=req_obj)
    final_req_users = final_req_obj.final_req_users.all()

    if(user_obj in final_req_users):
        final_req_obj.final_req_users.remove(user_obj)
        messages.info(request,"Request Removed!")
    else:
        final_req_obj.final_req_users.add(user_obj)
        messages.success(request,"Request Accepted Back, Now Details of Requester is Visible to You!")
    
    return redirect('connect:list-senders',id=req_obj.id)


# Displays the Contact After Match - Sender
@login_required
def view_contact_after_match_sender(request,id):
    req_obj = get_object_or_404(Request,pk=id)

    if req_obj.deleted:
        raise PermissionDenied()

    if (request.user.info.year != 1):
        if (req_obj.is_first_year_req):
            raise PermissionDenied()

    if (request.user.info.year == 1):
        if not (req_obj.is_first_year_req):
            raise PermissionDenied()
    
    if(req_obj.match_with_same_gender):
        if(request.user.info.gender != req_obj.requester.info.gender):
            raise PermissionDenied()
    
    final_req_obj,created1 = FinalMatchingRequest.objects.get_or_create(request=req_obj)
    final_req_users = final_req_obj.final_req_users.all()

    if not (request.user in final_req_users):
        messages.error(request,"You have Not Matched!")
        raise PermissionDenied()
    
    context = {
        'requester':req_obj.requester,
        'requesting':request.user
    }

    return render(request,'connect/contact-sharing.html',context=context)


# Displays the Contact After Match - Receiver
@login_required
def view_contact_after_match_receiver(request,id,username):
    req_obj = get_object_or_404(Request,pk=id)
    user_obj = get_object_or_404(User,username=username)

    if req_obj.deleted:
        raise PermissionDenied()

    if (request.user.info.year != 1):
        if (req_obj.is_first_year_req):
            raise PermissionDenied()

    if (request.user.info.year == 1):
        if not (req_obj.is_first_year_req):
            raise PermissionDenied()
    
    if(req_obj.match_with_same_gender):
        if(request.user.info.gender != req_obj.requester.info.gender):
            raise PermissionDenied()
    
    final_req_obj,created1 = FinalMatchingRequest.objects.get_or_create(request=req_obj)
    final_req_users = final_req_obj.final_req_users.all()

    if not (user_obj in final_req_users):
        messages.error(request,"You have Not Matched!")
        raise PermissionDenied()
    
    context = {
        'requester':user_obj,
        'requesting':request.user
    }

    return render(request,'connect/contact-sharing.html',context=context)


# Denies the Request of Sender
@login_required
def deny_request_view(request,id,username):
    req_obj = get_object_or_404(Request,pk=id)
    user_obj = get_object_or_404(User,username=username)

    if req_obj.deleted:
        raise PermissionDenied()

    if (request.user.info.year != 1):
        if (req_obj.is_first_year_req):
            raise PermissionDenied()

    if (request.user.info.year == 1):
        if not (req_obj.is_first_year_req):
            raise PermissionDenied()
    
    if(req_obj.match_with_same_gender):
        if(request.user.info.gender != req_obj.requester.info.gender):
            raise PermissionDenied()
    

    initial_req_obj,created = InitialMatchingRequest.objects.get_or_create(request=req_obj)
    initial_req_obj.req_users.remove(user_obj)

    return redirect('connect:list-senders',id=req_obj.id)