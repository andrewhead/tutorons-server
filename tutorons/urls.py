from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns(
    '',
    url(r'^$', 'tutorons.views.home', name='home'),
    url(r'^home$', 'tutorons.views.home', name='home'),
    url(r'^wget$', 'tutorons.views.wget', name='wget'),
    url(r'^css$', 'tutorons.views.css', name='css'),
    url(r'^regex$', 'tutorons.views.regex', name='regex'),
    url(r'^admin/', include(admin.site.urls)),
)
