from django.conf.urls import include, url
from . import views

app_name = "userPage"

urlpatterns = [
		url(r'^$', views.list, name='list'),
		url(r'^list/$', views.list, name='list'),
		#url(r'^test/$', 'test', name='test'),
]