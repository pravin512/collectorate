from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from localsite.models import AdhikariList, MeetingDetails
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import sys
import xlrd
from django import forms
import os 
import datetime
from collectorate.settings import STATICFILES_DIRS
from django.core.files.storage import FileSystemStorage

@login_required(login_url='user_login') #redirect when user is not logged in
def index(request):
    return render(request, 'index.html')

def user_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                request.session['username'] = username
                return HttpResponseRedirect(reverse('index'))
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return render(request, 'login.html')

@login_required(login_url='user_login') #redirect when user is not logged in
def adhikari_list(request, meeting_type):
    adhikariList = AdhikariList.objects.filter(type=meeting_type, status=1)
    return render(request, 'officers_list.html', {'adhikariList':adhikariList, 'meeting_type':meeting_type})

@login_required(login_url='user_login') #redirect when user is not logged in
def meeting_list(request, adhikari_id):
    adhikari = AdhikariList.objects.filter(adhikari_id=adhikari_id, status=1)
    if adhikari.exists():
        meeting_list = MeetingDetails.objects.filter(adhikari_id=adhikari[0], status=1).order_by('added_date_time')
        if len(meeting_list) > 0:
            page = request.GET.get('page', 1)

            paginator = Paginator(meeting_list, 1)
            try:
                meetings = paginator.page(page)
            except PageNotAnInteger:
                meetings = paginator.page(1)
            except EmptyPage:
                meetings = paginator.page(paginator.num_pages)
            
            pending_days = day_difference(meetings[0].marking_date, meetings[0].time_limit_date)
            return render(request, 'profile.html', {
                    'adhikari':adhikari,
                    'meeting':meetings,
                    'pending_days':pending_days
                    })
    return render(request, 'profile.html', {
                'adhikari':adhikari,
                'meeting':'',
                'pending_days':'--'
                })

def day_difference(from_date, to_date):
    delta = to_date - from_date
    return delta.days

def import_adhikari(request):
    dir_path = os.path.dirname(os.path.realpath(__file__)) 
    if request.method == 'POST':
        file_upload = handle_uploaded_file(dir_path+'/adhikari_template.xlsx', request.FILES['adhikariSheet'])
        if file_upload:
            book = xlrd.open_workbook(dir_path+'/adhikari_template.xlsx')
            sheet = book.sheet_by_index(0)

            if sheet.nrows > 51:
                return JsonResponse({'status':False, 'message':'maximum 50 rows allowed in single upload.'})
            # read first row for keys  
            keys = sheet.row_values(0)

            if len(keys) != 3:
                return JsonResponse({'status':False, 'message':'Invalid template'})

            if keys[0] != 'adhikari_name':
                return JsonResponse({'status':False, 'message':'Please add "adhikari_name" as 1st column'})
            if keys[1] != 'mobile':
                return JsonResponse({'status':False, 'message':'Please add "mobile" as 2nd column'})
            if keys[2] != 'designation':
                return JsonResponse({'status':False, 'message':'Please add "designation" as 3rd column'})
            
            # read the rest rows for values
            values = [sheet.row_values(i) for i in range(1, sheet.nrows)]
            dict_list = []
            for value in values:
                dict_list.append(dict(zip(keys, value)))

            adhikari_type = request.POST['adhikari_type']

            for adhikari in dict_list:
                adhikari_name = adhikari['adhikari_name']
                mobile = int(adhikari['mobile'])
                designation = adhikari['designation']
                
                AdhikariList.objects.create(adhikari_name=adhikari_name, mobile=mobile, designation=designation, type=adhikari_type)
            
            return JsonResponse({'status':True, 'message':'success'})
        else:
            return JsonResponse({'status':False, 'message':'Upload error, Please Refresh the page & try again!'})
    else:
        return JsonResponse({'status':False, 'message':'Please upload the file'})

def import_meeting(request):
    dir_path = os.path.dirname(os.path.realpath(__file__)) 
    if request.method == 'POST':
        file_upload = handle_uploaded_file(dir_path+'/meeting_template.xlsx', request.FILES['meetingSheet'])
        if file_upload:
            book = xlrd.open_workbook(dir_path+'/meeting_template.xlsx')
            sheet = book.sheet_by_index(0)

            if sheet.nrows > 51:
                return JsonResponse({'status':False, 'message':'maximum 50 rows allowed in single upload.'})

            # read first row for keys  
            keys = sheet.row_values(0)

            if len(keys) != 4:
                return JsonResponse({'status':False, 'message':'Invalid template'})

            if keys[0] != 'marking_date':
                return JsonResponse({'status':False, 'message':'Please add "marking_date" as 1st column'})
            if keys[1] != 'limit_date':
                return JsonResponse({'status':False, 'message':'Please add "limit_date" as 2nd column'})
            if keys[2] != 'description':
                return JsonResponse({'status':False, 'message':'Please add "description" as 3rd column'})
            if keys[3] != 'document_link':
                return JsonResponse({'status':False, 'message':'Please add "document_link" as 4th column'})
            
            # read the rest rows for values
            values = [sheet.row_values(i) for i in range(1, sheet.nrows)]
            dict_list = []
            for value in values:
                dict_list.append(dict(zip(keys, value)))

            adhikari = AdhikariList.objects.get(pk=int(request.POST['adhikari_id']))

            for meeting in dict_list:
                marking_date = datetime.datetime(*xlrd.xldate_as_tuple(meeting['marking_date'], book.datemode))
                limit_date = datetime.datetime(*xlrd.xldate_as_tuple(meeting['limit_date'], book.datemode))
                description = meeting['description']
                link = meeting['document_link']
                
                MeetingDetails.objects.create(adhikari_id=adhikari, marking_date=marking_date, time_limit_date=limit_date, description=description, url=link)
            
            return JsonResponse({'status':True, 'message':'success'})
        else:
            return JsonResponse({'status':False, 'message':'Upload error, Please Refresh the page & try again!'})
    else:
        return JsonResponse({'status':False, 'message':'Please upload the file'})


def delete_meetings(request):
    MeetingDetails.objects.filter(meeting_id=request.POST['meeting_id']).update(status=0)
    return JsonResponse({'status':False, 'message':'deleted'})

def delete_adhikari(request):
    MeetingDetails.objects.filter(adhikari_id=request.POST['adhikari_id']).update(status=0)
    AdhikariList.objects.filter(adhikari_id=request.POST['adhikari_id']).update(status=0)
    return JsonResponse({'status':False, 'message':'deleted'})

def handle_uploaded_file(dir_path, f):
    with open(dir_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return True

def update_adhikari(request):
    AdhikariList.objects.filter(adhikari_id=request.POST['adhikari_id']).update(adhikari_name=request.POST['adhikari_name'], mobile=request.POST['adhikari_mobile'], designation=request.POST['adhikari_designation'])
    return JsonResponse({'status':False, 'message':'Updated'})

def update_meeting(request):
    MeetingDetails.objects.filter(meeting_id=request.POST['meeting_id']).update(marking_date=request.POST['marking_date'], time_limit_date=request.POST['time_limit_date'], url=request.POST['document_url'], description=request.POST['description'])
    return JsonResponse({'status':False, 'message':'Updated'})

def change_profile_image(request):
    if request.method == 'POST' and request.FILES['profile_image']:
        myfile = request.FILES['profile_image']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        AdhikariList.objects.filter(adhikari_id=request.POST['adhikari_id']).update(img_url=uploaded_file_url)
    return JsonResponse({'status':False, 'message':'Updated'})