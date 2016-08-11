from django.conf.urls import patterns, include, url

urlpatterns = patterns('userPage.views',
		url(r'^$', 'list', name='list'),
		url(r'^list/$', 'list', name='list'),
		#url(r'^test/$', 'test', name='test'),
)