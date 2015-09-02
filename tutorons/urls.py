from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns(
    '',
    url(r'^$', 'tutorons.views.home', name='home'),
    url(r'^home$', 'tutorons.views.home', name='home'),
    url(r'^wget$', 'tutorons.views.wget', name='wget'),
    url(r'^css$', 'tutorons.views.css', name='css'),
    url(r'^regex$', 'tutorons.views.regex', name='regex'),
    url(r'^explain/wget$', 'tutorons.views.explain_wget', name='explain_wget'),
    url(r'^explain/css$', 'tutorons.views.explain_css', name='explain_css'),
    url(r'^explain/regex$', 'tutorons.views.explain_regex', name='explain_regex'),
    url(r'^admin/', include(admin.site.urls)),
)
