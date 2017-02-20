from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from admin.views import views
from api.views import api

urlpatterns = [
    url(r'^login$', views.login),
    url(r'^logout/$', views.logout),
    url(r'^admin/$', views.admin),
    url(r'^admin/post/list$', views.postList),
    url(r'^admin/post/(?P<id>\d+)$', views.postDetail),
    url(r'^admin/post/edit/(?P<id>\d+)$', views.postUpdate),
    url(r'^admin/post/new$', views.newPost),
    url(r'^admin/post/delete/(?P<id>\d+)$', views.postDelete),

    url(r'^api/login$', api.login),
    url(r'^api/post/list$', api.postList),
    url(r'^api/post/(?P<id>\d+)/like$', api.like),
    url(r'^api/post/(?P<id>\d+)/participate$', api.participate),
    url(r'^api/post/(?P<id>\d+)/comment$', api.participate),

    url(r'^.*$', views.notDefinedUrl),
]