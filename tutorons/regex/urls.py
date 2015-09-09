from django.conf.urls import patterns, url


urlpatterns = patterns(
    '',
    url(r'^scan$', 'tutorons.regex.views.scan', name='regex_scan'),
    url(r'^explain$', 'tutorons.regex.views.explain', name='regex_explain'),
)
