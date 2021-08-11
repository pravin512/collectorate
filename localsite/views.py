from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from localsite.models import AdhikariList, MeetingDetails
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import sys
import xlrd
# from lomodels import AdhikariList

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
    return render(request, 'officers_list.html', {'adhikariList':adhikariList})

@login_required(login_url='user_login') #redirect when user is not logged in
def meeting_list(request, adhikari_id):
    adhikari = AdhikariList.objects.get(pk=adhikari_id)
    if adhikari:
        meeting_list = MeetingDetails.objects.filter(adhikari_id=adhikari).order_by('added_date_time')
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

def import_meeting(request):
    import os 
    import datetime
    dir_path = os.path.dirname(os.path.realpath(__file__))  

    book = xlrd.open_workbook(dir_path+'/meeting_template.xlsx')
    sheet = book.sheet_by_index(0)

    # read first row for keys  
    keys = sheet.row_values(0)

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
    
    return JsonResponse({'status':True})

