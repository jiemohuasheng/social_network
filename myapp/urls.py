from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'myapp'

urlpatterns = [
                  url(r'^login[/]$', views.user_authn, name='login'),
                  url(r'^logout[/]$', views.user_logout, name='logout'),
                  url(r'^forgot-password[/]$', views.forgot_password, name='forgot_password'),
                  url(r'^$', views.index, name='index'),
                  url(r'^myprofile[/]$', views.my_prof, name='userprofile'),
                  url(r'^explore[/]$', views.explore_viw, name='explore'),
                  url(r'^postdetail/(?P<id>\d*)$', views.postdetail_viw, name='postdetail'),
                  url(r'^addpost[/]$', views.addpost_viw, name='addpost'),
                  url(r'^useredit[/]$', views.useredit_viw, name='useredit'),
                  url(r'^userprofile/(?P<id>\d*)$', views.user_prof, name='userprofile'),
                  url(r'^messages/(?P<id>\d*)$', views.message_view, name='messages'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
