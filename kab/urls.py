from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
#     url(r'^admin/', include(admin.site.urls)),
#     url(r'^zohar/', include('zohar.urls')),
#     url(r'', include('zohar.urls'))
    url(r'^admin/', admin.site.urls),
    url(r'^zohar/', 'zohar.urls'),
    url(r'', 'zohar.urls')
]
