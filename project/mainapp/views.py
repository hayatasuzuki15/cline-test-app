from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.utils import timezone
from .models import Attendance
from django.contrib.auth.decorators import login_required

from django.http import HttpResponseNotFound

def home(request):
    return render(request, 'home.html')

def signup(request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')

def page_not_found(request, exception):
    return redirect('home')

@login_required
def clock_in(request):
    attendance, created = Attendance.objects.get_or_create(user=request.user, clock_out_time__isnull=True)
    if created:
        attendance.clock_in_time = timezone.now()
        attendance.save()
    return redirect('attendance')

@login_required
def clock_out(request):
    try:
        attendance = Attendance.objects.get(user=request.user, clock_out_time__isnull=True)
        attendance.clock_out_time = timezone.now()
        attendance.save()
    except Attendance.DoesNotExist:
        pass
    return redirect('attendance')

@login_required
def attendance(request):
    records = Attendance.objects.filter(user=request.user).order_by('-clock_in_time')
    return render(request, 'attendance/attendance.html', {'records': records})
