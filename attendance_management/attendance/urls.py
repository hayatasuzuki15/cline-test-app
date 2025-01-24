from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AttendanceViewSet, login_view, dashboard_view, logout_view


router = DefaultRouter()
router.register(r"attendance", AttendanceViewSet)

urlpatterns = [
    path("", login_view, name="login"),
    path("dashboard/", dashboard_view, name="dashboard"),
    path("logout/", logout_view, name="logout"),
    path("api/", include(router.urls)),
]
