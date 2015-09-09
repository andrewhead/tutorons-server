from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns(
    '',
    url(r'^$', 'tutorons.views.home', name='home'),
    url(r'^home$', 'tutorons.views.home', name='home'),
    url(r'^wget/', include('tutorons.wget.urls')),
    url(r'^css/', include('tutorons.css.urls')),
    url(r'^regex/', include('tutorons.regex.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
