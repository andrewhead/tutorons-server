from django.conf.urls import patterns, url


urlpatterns = patterns(
    '',
    url(r'^scan$', 'tutorons.python.views.scan', name='python_scan'),
    url(r'^explain$', 'tutorons.python.views.explain', name='python_explain'),
)
