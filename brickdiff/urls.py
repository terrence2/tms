from django.conf.urls import patterns, url

from brickdiff import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^diff/$', views.diff, name='diff'),
    url(r'^result/$', views.result, name='result'),
)
