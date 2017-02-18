from django.conf.urls import patterns, include, url
from admin.views import views

urlpatterns = patterns('',
 	url(r'^static/(?P<path>.*)$', 'django.views.static.serve',),  
  url(r'^login/$', views.login),
  url(r'^logout/$', views.logout),
  url(r'^admin/$', views.admin),
  url(r'^admin/post/list$', views.postList),
  url(r'^admin/post/(?P<id>\d+)/$', views.postDetail),
  url(r'^admin/post/edit/(?P<id>\d+)$', views.postUpdate),
  url(r'^admin/post/new$', views.newPost),
  url(r'^admin/post/delete/(?P<id>\d+)$', views.postDelete),
)
