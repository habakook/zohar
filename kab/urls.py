from django.urls import path, re_path
from django.contrib import admin
from zohar.views import index, stats

urlpatterns = [
    path('admin/', admin.site.urls),
    path('mySecretStats8472/', stats),
    re_path(r'^zohar/', index),
    re_path(r'', index),
]
