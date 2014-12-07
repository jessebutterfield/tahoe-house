from django.template import Context, loader, RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from booktahoe.models import Night, Comment, Guest, Attending, UserAttributes
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from datetime import datetime,date,timedelta
from django import forms
import calendar

# Create your views here.

mnames = "January February March April May June July August September October November December"
mnames = mnames.split()

def index(request):
    return HttpResponse("Not sure how you got here. This page was just for debugging.")
    
def postLogin(request):
    form = AuthenticationForm(request,data=request.POST)
    if(form.is_valid()):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        n = request.POST['next']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            ua,created = UserAttributes.objects.get_or_create(user=user)
            if(created):
                return HttpResponseRedirect(reverse('booktahoe.views.updateInfo'))
            else:
                if(n):
                    return HttpResponseRedirect(n)
                else:
                    return HttpResponseRedirect(reverse('booktahoe.views.currentMonth'))
        HttpResponse("Form was valid")
    return HttpResponse("Form was invalid")

def updateInfo(request, form = None):
    if(not form):
        formClass = info_form_factory(request.user)
        form = formClass()
    return render_to_response('nights/userUpdate.html', {'form':form},
                              context_instance=RequestContext(request))
    
def saveInfo(request):
    user = request.user
    formClass = info_form_factory(user)
    form = formClass(request.POST)
    if(form.is_valid()):
        user.username = form.cleaned_data['username']
        p = form.cleaned_data['password']
        if(p):
            user.set_password(p)
        sigOther = form.cleaned_data['sigOther']
        user.save()
        ua,_ = UserAttributes.objects.get_or_create(user=user)
        ua.sigMember = sigOther
        ua.save()
        return HttpResponseRedirect(reverse('booktahoe.views.currentMonth'))
    else:
        return updateInfo(request, form)

def info_form_factory(user):
    class UserInfoForm(forms.Form):
        choices = User.objects.filter(is_active=True)
        choiceSet = [(-1,'Not Dating a Member')]
        choiceSet.extend(choices.values('id','username'))
        username = forms.CharField(initial=user.username)
        password = forms.CharField(label='New Password',widget=forms.PasswordInput,required=False)
        check = forms.CharField(label='Retype Password',widget=forms.PasswordInput,required=False)
        if(hasattr(user,'userattributes') and user.userattributes.sigMember):
            ini = user.userattributes.sigMember
        else:
            ini = None
        sigOther = forms.ModelChoiceField(label='Significant Other',empty_label="Not Dating a Member",
                                          queryset=User.objects.all(), initial=ini,required=False)
        def clean(self):
            cleaned_data = super(UserInfoForm, self).clean()
            if(cleaned_data.get("password") != cleaned_data.get("check")):
                raise forms.ValidationError('Passwords do not match')
            return cleaned_data
    return UserInfoForm

def detail(request, year, month, day, commentId = False):
    if(commentId):
        commentId = int(commentId)
    datename = year + "-" + month + "-" + day
    year, month, day = int(year), int(month), int(day)
    d = date(year,month,day)
    n,_ = Night.objects.get_or_create(night = d)
    attends = Attending.objects.filter(night = n)
    guestList = []
    for g in Guest.objects.filter(attend__night=n):
        #TODO: this violates good practices
        guestList.append(g.name +' ('+ g.attend.member.username+')')
    if(request.user.is_authenticated()):
        a = Attending.objects.filter(night = n,member = request.user)
        coming = a.exists()
        guestString = ''
        p = 0
        plusOne = False
        if(coming):
            a = a[0]
            plusOne = a.plusOne
            p = a.parkingRequests
            guests = Guest.objects.filter(attend = a)       
            for guest in guests:
                guestString += guest.name +'\n'
        formClass = my_form_factory(initComing=coming,initGuests=guestString,initParking=p,sigOther=plusOne)
        form = formClass()
    else:
        form = False
    return render_to_response('nights/detail.html', 
                              {'year':year,'month':month,'day':day,'attends': attends, 'night': n,
                               'datename':datename,'form':form, 'guestList':guestList,
                               'commentId':commentId},
                              context_instance=RequestContext(request))
    
def my_form_factory(initComing=False,initNights=1,initGuests='',initParking=0,sigOther=False):
    class BookingForm(forms.Form):
        coming = forms.BooleanField(required=False,initial=initComing)
        plusOne = forms.BooleanField(required=False,initial=sigOther,label='With significant other?')
        nights = forms.IntegerField(min_value=1,initial=initNights)
        parking = forms.IntegerField(min_value=0, initial=initParking)
        guests = forms.CharField(required=False,initial=initGuests,
                                 widget=forms.Textarea(attrs={'cols': 20, 'rows': 6}))
    return BookingForm

    
def book(request,night_id):
    if(request.user.is_authenticated()):
        formClass = my_form_factory()
        form = formClass(request.POST)
        if(form.is_valid()):
            n = get_object_or_404(Night, pk=night_id)
            booknight(request,form,n)
            nights = form.cleaned_data['nights']
            nights -= 1
            nextNight = n.night
            while(nights > 0):
                nextNight = nextNight + timedelta(days=1)
                n2, _ = Night.objects.get_or_create(night=nextNight)
                booknight(request,form,n2)
                nights -= 1
            d = n.night
            return HttpResponseRedirect(reverse('booktahoe.views.month', args=(d.year,d.month,)))
        else:
            HttpResponse(form.coming.error_messages+form.guests.error_messages+form.nights.error_messages)
    return HttpResponseRedirect(reverse('booktahoe.views.index'))

def booknight(request,form,n):
    coming = form.cleaned_data['coming']
    plusOne = form.cleaned_data['plusOne']
    user = request.user
    if(coming):
        a, _ = Attending.objects.get_or_create(member=user,night=n)
        a.plusOne=plusOne
        if(plusOne and user.userattributes.sigMember):
            b, _ = Attending.objects.get_or_create(member=user.userattributes.sigMember,night=n)
            b.plusOne = plusOne
            b.save()
        parkingSlots = form.cleaned_data['parking']
        a.parkingRequests = parkingSlots
        Guest.objects.filter(attend=a).delete()
        guests = form.cleaned_data['guests']
        guests = guests.splitlines()
        for guest in guests:
            if(guest and not guest.isspace()):
                Guest.objects.create(name=guest,attend=a)
        a.save()
    else:
        Attending.objects.filter(night=n,member=user).delete()
        if(plusOne and user.userattributes.sigMember):
            Attending.objects.filter(night=n,member=user.userattributes.sigMember).delete()  

def deleteComment(request,comment_id):
    if(not request.user.is_authenticated()):
        return HttpResponseRedirect(reverse('django.contrib.auth.views.login'))
    try:
        c = Comment.objects.get(pk=comment_id)
        d = c.night.night
        if(c.poster.id == request.user.id):
            c.delete()
        return HttpResponseRedirect(reverse('booktahoe.views.detail', args=(d.year,d.month,d.day,))+'#c')   
    except ObjectDoesNotExist:
        return currentMonth(request)        

def editComment(request,comment_id):
    if( not request.user.is_authenticated()):
        return HttpResponseRedirect(reverse('django.contrib.auth.views.login'))
    try:
        c = Comment.objects.get(pk=comment_id)
        d = c.night.night
        if(c.poster.id == request.user.id):
            text = request.POST['commentText']
            c.text = text
            c.save()
        return HttpResponseRedirect(reverse('booktahoe.views.detail', 
                                            args=(d.year,d.month,d.day))+'#c'+str(c.id))   
    except ObjectDoesNotExist:
        return currentMonth(request)   
    
def comment(request,night_id):
    if(request.user.is_authenticated()):
        night = get_object_or_404(Night, pk=night_id)
        text = request.POST['commentText']
        com = Comment(night=night,poster=request.user,text=text)#,created=datetime.now())
        com.save()
        d = night.night
        return HttpResponseRedirect(reverse('booktahoe.views.detail', 
                                            args=(d.year,d.month,d.day))+'#c'+str(com.id))
    else:
        return HttpResponseRedirect(reverse('booktahoe.views.index'))

def newMonth(request, year, month, change):
    year, month = int(year), int(month)
    if change in ("next", "prev"):
        d, mdelta = date(year, month, 15), timedelta(days=31)
        if change == "next":   
            d += mdelta
        elif change == "prev": 
            d -= mdelta
        year, month = d.timetuple()[0:2]
    return HttpResponseRedirect(reverse('booktahoe.views.month', args=(year,month)))
   
def currentMonth(request):
    year, month = date.today().timetuple()[0:2]
    return HttpResponseRedirect(reverse('booktahoe.views.month', args=(year,month)))
    
def month(request, year, month):
    """Listing of days in `month`."""
    year, month = int(year), int(month)


    # init variables
    cal = calendar.Calendar()
    cal.setfirstweekday(6)
    month_days = cal.itermonthdays(year, month)
    lst = [[]]
    week = 0

    # make month lists containing list of days for each week
    # each day tuple will contain list of entries and 'current' indicator
    today = datetime.now()
    for day in month_days:
        entries = current = False   # are there entries for this day; current day?
        guests = 0
        parking = 0
        if day:
            #TODO: fix this to a get and a try 
            n = date(year,month,day)
            entries = Night.objects.filter(night=n)
            if(entries):
                for u in entries[0].attendees.all():
                    a = u.attending_set.get(night=entries[0])
                    parking += a.parkingRequests
                    guests += a.guest_set.count()
            if(today.year == year and today.month == month and today.day == day):
                current = True

        lst[week].append((day, entries,current,guests,parking))
        if len(lst[week]) == 7:
            lst.append([])
            week += 1

    return render_to_response("nights/month.html", dict(year=year, month=month, user=request.user,
                        month_days=lst, mname=mnames[month-1]))