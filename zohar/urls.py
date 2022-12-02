# from django.conf.urls import patterns, url

# from zohar import views

# urlpatterns = patterns('',
# url(r'^$', views.index, name='index'),
# # ex: /zohar/5/
# #url(r'^(?P<book_number>\d+)/$', views.book, name='view_book'),
# )
from django.conf.urls import *
from django.contrib import admin
from zohar import views
admin.autodiscover()

# urlpatterns = [
#     url(r'^$', views.index, name='index'),
# ]
urlpatterns = [
#     path(r'^$', views.index),
    re_path(r'^$', views.index),
]
