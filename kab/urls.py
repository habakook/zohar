# from django.conf.urls import patterns, include, url

# from django.contrib import admin
# admin.autodiscover()

# urlpatterns = patterns('',
#     # Examples:
#     # url(r'^$', 'kab.views.home', name='home'),
#     # url(r'^blog/', include('blog.urls')),
#     url(r'^admin/', include(admin.site.urls)),
#     url(r'^zohar/', include('zohar.urls')),
# )
from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^zohar/', include('zohar.urls')),
]
