from django.contrib import admin
from django.urls import path, include  # includeをインポート

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mainapp.urls')),  # mainappのURLをインクルード
]
