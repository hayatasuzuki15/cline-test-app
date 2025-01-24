from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('clock_in/', views.clock_in, name='clock_in'),
    path('clock_out/', views.clock_out, name='clock_out'),
    path('attendance/', views.attendance, name='attendance'),
]
