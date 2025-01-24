import os
import django
from django.conf import settings

# Django設定モジュールを環境変数から読み込む
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "attendance_management.settings")

# Djangoの設定を読み込む
django.setup()
