from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.views import LoginView
from .models import Attendance, WorkHour

class CustomLoginView(LoginView):
    template_name = 'login.html'

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')  # ホームページにリダイレクト
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def home(request):
    return render(request, 'home.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')  # ホームページにリダイレクト

@login_required
def check_in(request):
    attendance, created = Attendance.objects.get_or_create(user=request.user, check_out=None)
    if created:
        attendance.check_in = timezone.now()
        attendance.save()
    return redirect('home')

@login_required
def check_out(request):
    attendance = Attendance.objects.filter(user=request.user, check_out=None).first()
    if attendance:
        attendance.check_out = timezone.now()
        attendance.save()
    return redirect('home')

@login_required
def record_work_hours(request):
    attendance = Attendance.objects.filter(user=request.user).last()
    if attendance and attendance.check_out:
        work_hour = WorkHour(user=request.user, date=attendance.check_in.date(), hours_worked=(attendance.check_out - attendance.check_in).total_seconds() / 3600)
        work_hour.save()
    return redirect('home')

@login_required
def work_history(request):
    work_hours = WorkHour.objects.filter(user=request.user).order_by('-date')
    return render(request, 'work_history.html', {'work_hours': work_hours})

@login_required
def attendance_page(request):
    return render(request, 'attendance.html')
