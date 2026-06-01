from django.urls import path, re_path
from django.contrib import admin
from zohar.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^zohar/', index),
    re_path(r'', index),
]
