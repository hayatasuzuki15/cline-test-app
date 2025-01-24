from django.urls import path
from .views import register, home, logout_view, check_in, check_out, record_work_hours, work_history, CustomLoginView, attendance_page

urlpatterns = [
    path('register/', register, name='register'),
    path('', home, name='home'),
    path('logout/', logout_view, name='logout'),  # ログアウト用のURLを追加
    path('checkin/', check_in, name='check_in'),  # 出勤打刻用のURLを追加
    path('checkout/', check_out, name='check_out'),  # 退勤打刻用のURLを追加
    path('record_work_hours/', record_work_hours, name='record_work_hours'),  # 勤務時間記録用のURLを追加
path('attendance/', attendance_page, name='attendance'),  # 打刻用のURLを追加
    path('login/', CustomLoginView.as_view(), name='login'),  # ログイン用のURLを追加
]
