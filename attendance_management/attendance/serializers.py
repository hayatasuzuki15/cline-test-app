from rest_framework import serializers
from .models import Attendance
from django.contrib.auth.models import User
from django.utils import timezone


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class AttendanceSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    date = serializers.DateField(read_only=True)
    clock_in = serializers.DateTimeField(read_only=True)
    clock_out = serializers.DateTimeField(
        required=False, allow_null=True, read_only=True
    )

    class Meta:
        model = Attendance
        fields = ["id", "user", "clock_in", "clock_out", "work_duration", "date"]

    def create(self, validated_data):
        # ユーザーを取得
        user = self.context["request"].user

        # 現在の日付と時間を使用
        now = timezone.now()

        # 新しいAttendanceインスタンスを作成
        attendance = Attendance.objects.create(user=user, date=now.date(), clock_in=now)

        return attendance

    def update(self, instance, validated_data):
        # 退勤処理の場合
        if not instance.clock_out:
            instance.clock_out = timezone.now()
            instance.save()

        return instance
