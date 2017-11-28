from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView

urlpatterns = patterns('',
    #url(r'^$', TemplateView.as_view(template_name='index.html'), name="home"),
    #url(r'^spatialtest/', include('SpatialReasoningTest.urls')),
    #url(r'^', include('SIIPproject.urls')),
    url(r'^spatialtest/', include('SIIPproject.urls')),
    url(r'^', include('SIIPproject.urls')),
    #url(r'^shib/', include('shibboleth.urls', namespace='shibboleth')),
)
