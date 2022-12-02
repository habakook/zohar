from django.conf.urls import include, url
from django.urls import path, re_path

from django.contrib import admin
from zohar.views import index

admin.autodiscover()

urlpatterns = [
#     url(r'^admin/', include(admin.site.urls)),
#     url(r'^zohar/', include('zohar.urls')),
#     url(r'', include('zohar.urls'))
    url(r'^admin/', admin.site.urls),
    url(r'^zohar/', index),
    url(r'', index)
]
