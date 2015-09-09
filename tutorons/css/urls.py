from django.conf.urls import patterns, url


urlpatterns = patterns(
    '',
    url(r'^scan$', 'tutorons.css.views.scan', name='css_scan'),
    url(r'^explain$', 'tutorons.css.views.explain', name='css_explain'),
)
