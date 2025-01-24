import os
import django
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from attendance.models import Attendance
from django.utils import timezone

# Django設定を明示的に読み込む
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "attendance_management.settings")
django.setup()


class ClockInTestCase(TestCase):
    def setUp(self):
        # テスト用のユーザーを作成
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

        # APIクライアントを設定
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # クロックインのURL
        self.clock_in_url = reverse("attendance-clock-in")

    def test_successful_clock_in(self):
        """正常な出勤打刻のテスト"""
        response = self.client.post(self.clock_in_url)

        # レスポンスのステータスコードを確認
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # データベースに新しいAttendanceレコードが作成されたことを確認
        attendance = Attendance.objects.filter(user=self.user).first()
        self.assertIsNotNone(attendance)

        # 日付と出勤時間が正しいことを確認
        self.assertEqual(attendance.date, timezone.now().date())
        self.assertIsNotNone(attendance.clock_in)

    def test_duplicate_clock_in(self):
        """同日に2回出勤打刻しようとした場合のテスト"""
        # 最初の出勤打刻
        self.client.post(self.clock_in_url)

        # 2回目の出勤打刻
        response = self.client.post(self.clock_in_url)

        # エラーレスポンスを確認
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], "既に出勤済みです。")

        # データベース内のレコード数が1であることを確認
        self.assertEqual(Attendance.objects.filter(user=self.user).count(), 1)

    def test_clock_in_without_authentication(self):
        """認証なしでの出勤打刻のテスト"""
        # 認証を解除
        self.client = APIClient()  # 新しいクライアントを作成

        response = self.client.post(self.clock_in_url)

        # 認証エラーを確認（DjangoRFのデフォルトは403 Forbidden）
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_clock_in_date_and_time(self):
        """出勤打刻の日付と時間の正確性テスト"""
        response = self.client.post(self.clock_in_url)

        attendance = Attendance.objects.filter(user=self.user).first()

        # 日付が今日であることを確認
        self.assertEqual(attendance.date, timezone.now().date())

        # 出勤時間が現在時刻に近いことを確認（数秒の誤差を許容）
        now = timezone.now()
        time_diff = abs((attendance.clock_in - now).total_seconds())
        self.assertLess(time_diff, 5)  # 5秒以内であれば許容
