from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Attendance
from .serializers import AttendanceSerializer
from django.utils import timezone


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "ユーザー名またはパスワードが正しくありません。")

    return render(request, "attendance/login.html")


@login_required
def dashboard_view(request):
    return render(request, "attendance/dashboard.html")


def logout_view(request):
    logout(request)
    return redirect("login")


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        # シリアライザーにリクエストコンテキストを渡す
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def get_queryset(self):
        return Attendance.objects.filter(user=self.request.user)

    @action(detail=False, methods=["POST"])
    def clock_in(self, request):
        user = request.user
        today = timezone.now().date()

        # 既に今日の出勤レコードがあるかチェック
        existing_attendance = Attendance.objects.filter(
            user=user, date=today, clock_out__isnull=True
        ).first()

        if existing_attendance:
            return Response(
                {"detail": "既に出勤済みです。"}, status=status.HTTP_400_BAD_REQUEST
            )

        # シリアライザーを使用してAttendanceを作成
        serializer = self.get_serializer(data={})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    @action(detail=False, methods=["POST"])
    def clock_out(self, request):
        user = request.user
        today = timezone.now().date()

        # 今日の未退勤のレコードを取得
        attendance = Attendance.objects.filter(
            user=user, date=today, clock_out__isnull=True
        ).first()

        if not attendance:
            return Response(
                {"detail": "出勤打刻がありません。"}, status=status.HTTP_400_BAD_REQUEST
            )

        # シリアライザーを使用してAttendanceを更新
        serializer = self.get_serializer(attendance)
        serializer.update(attendance, {})

        return Response(serializer.data)
