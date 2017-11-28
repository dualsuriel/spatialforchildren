from django.conf.urls import include, url
from SIIPproject.views import IntroView, GradebookView, TestView, LogView, ThankuView, SurveyView, Survey2View,Survey3View, Survey4View, TestsummaryView, Announcements

urlpatterns = (
	url(r'^$', 'SIIPproject.views.index', name='redirect'),
	url(r'^index/$', 'SIIPproject.views.index', name='index'),
	url(r'^login/$', 'SIIPproject.views.index', name='login'),
	url(r'^announcements/$', 'SIIPproject.views.Announcements', name='Announcements'),
	url(r'^intro/$', IntroView.as_view(), name='intro'),
	url(r'^uploadlog$', 'SIIPproject.views.upload', name='upload'),
	url(r'^downloadlog/$', 'SIIPproject.views.download', name='download'),
	url(r'^gradebook/$', GradebookView.as_view(), name='gradebook'),
	url(r'^survey/$', SurveyView.as_view(), name='survey'),
	url(r'^survey2/$', Survey2View.as_view(), name='survey2'),
	url(r'^survey3/$', Survey3View.as_view(), name='survey3'),
	url(r'^survey4/$', Survey4View.as_view(), name='survey3'),
	url(r'^testsummary/$', TestsummaryView.as_view(), name='testsummary'),
	url(r'^test/$', TestView.as_view(), name='test'),
	url(r'^log/', LogView.as_view(), name='log'),
	url(r'^thanku/$', ThankuView.as_view(), name='thanku'),
)
