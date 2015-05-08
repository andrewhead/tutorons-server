from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tutorons.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^wget$', 'tutorons.views.wget', name='wget'),
    url(r'^css$', 'tutorons.views.css', name='css'),
    url(r'^admin/', include(admin.site.urls)),
)
