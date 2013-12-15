from django.template import Context, loader, RequestContext
from django.shortcuts import render
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from booktahoe.models import Night, Comment, Guest
from datetime import datetime,date,timedelta
from django import forms
import calendar

# Create your views here.

mnames = "January February March April May June July August September October November December"
mnames = mnames.split()

def index(request):
    return HttpResponse("Hello, world. You're at the poll index.")

def detail(request, year, month, day):
    datename = year + "-" + month + "-" + day
    year, month, day = int(year), int(month), int(day)
    d = date(year,month,day)
    n,created = Night.objects.get_or_create(night = d)
    coming = request.user in set(n.members.all())
    guests = Guest.objects.filter(night=n,host=request.user)
    guestString = ''
    for guest in guests:
        guestString + guest.name +'/n'
    formClass = my_form_factory(initComing=coming,initGuests=guestString)
    form = formClass()
    return render_to_response('nights/detail.html', 
                              {'night': n,'datename':datename,'form':form},
                              context_instance=RequestContext(request))
    
def my_form_factory(initComing=False,initNights=1,initGuests=''):
    class BookingForm(forms.Form):
        coming = forms.BooleanField(required=False,initial=initComing)
        nights = forms.IntegerField(min_value=1,initial=initNights)
        guests = forms.CharField(required=False,initial=initGuests,
                                 widget=forms.Textarea(attrs={'cols': 20, 'rows': 6}))
    return BookingForm

    
def book(request,night_id):
    if(request.user.is_authenticated()):
        formClass = my_form_factory()
        form = formClass(request.POST)
        if(form.is_valid()):
            n = get_object_or_404(Night, pk=night_id)
            coming = form.cleaned_data['coming']
            if(coming):
                n.members.add(request.user)
            else:
                n.members.remove(request.user)
            guests = form.cleaned_data['guests']
            guests = guests.splitlines()
            for guest in guests:
                if(guest and not guest.isspace()):
                    if(coming):
                        g = Guest.objects.get_or_create(name=guest,night=n,host=request.user)
            d = n.night
            return HttpResponseRedirect(reverse('booktahoe.views.month', args=(d.year,d.month,)))
        else:
            HttpResponse(form.coming.error_messages+form.guests.error_messages+form.nights.error_messages)
    return HttpResponseRedirect(reverse('booktahoe.views.index'))

def comment(request,night_id):
    if(request.user.is_authenticated()):
        night = get_object_or_404(Night, pk=night_id)
        text = request.POST['commentText']
        com = Comment(night=night,poster=request.user,text=text)#,created=datetime.now())
        com.save()
        d = night.night
        return HttpResponseRedirect(reverse('booktahoe.views.detail', args=(d.year,d.month,d.day,)))
    else:
        return HttpResponseRedirect(reverse('booktahoe.views.index'))
    
def month(request, year, month, change=None):
    """Listing of days in `month`."""
    year, month = int(year), int(month)


    # init variables
    cal = calendar.Calendar()
    month_days = cal.itermonthdays(year, month)
    lst = [[]]
    week = 0

    # make month lists containing list of days for each week
    # each day tuple will contain list of entries and 'current' indicator
    today = datetime.today().date()
    for day in month_days:
        entries = current = False   # are there entries for this day; current day?
        if day:
            entries = Night.objects.filter(night=date(year,month,day))
            if(today.year == year and today.month == month and today.day == day):
                current = True

        lst[week].append((day, entries, current))
        if len(lst[week]) == 7:
            lst.append([])
            week += 1

    return render_to_response("nights/month.html", dict(year=year, month=month, user=request.user,
                        month_days=lst, mname=mnames[month-1]))