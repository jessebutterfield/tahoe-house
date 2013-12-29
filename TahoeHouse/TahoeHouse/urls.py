from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'TahoeHouse.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^nights/', include('booktahoe.urls')),
    url(r'', include('booktahoe.urls')),
    url(r'^admin/', include(admin.site.urls)),
)