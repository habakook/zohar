from django.conf.urls import include, url
from django.urls import path, re_path

from django.contrib import admin
from zohar.zohar.views import index

admin.autodiscover()

urlpatterns = [
#     url(r'^admin/', include(admin.site.urls)),
#     url(r'^zohar/', include('zohar.urls')),
#     url(r'', include('zohar.urls'))
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^zohar/', index),
    re_path(r'', index)
]
