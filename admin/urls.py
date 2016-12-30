from django.conf.urls import patterns, include, url
from admin.views import views

urlpatterns = patterns('',
 	url(r'^static/(?P<path>.*)$', 'django.views.static.serve',),  
  url(r'^login/$', views.login)
  
)
