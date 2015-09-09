from django.conf.urls import patterns, url


urlpatterns = patterns(
    '',
    url(r'^scan$', 'tutorons.wget.views.scan', name='wget_scan'),
    url(r'^explain$', 'tutorons.wget.views.explain', name='wget_explain'),
)
