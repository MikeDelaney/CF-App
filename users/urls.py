from django.conf.urls import patterns, url
from users import views, forms

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^user_list/$', views.user_list, name='user_list'),
	url(r'^register/$', views.register, name='register'),
	url(r'^add_user/$', views.add_user, name='add_user'),
	url(r'^login/$', views.user_login, name='login'),
	url(r'^logout/$', views.user_logout, name='logout'),
	url(r'^(?P<username>\w+)/$', views.user_edit, name='user_edit'),
)