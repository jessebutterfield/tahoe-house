from django.conf.urls import patterns, url

from booktahoe import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    # ex: /nights/5/
    url(r"^(\d+)/(\d+)/(\d+)/$", views.detail, name='detail'),
    url(r"^(\d+)/(\d+)/$", views.month, name='month'),
    url(r'^(?P<night_id>\d+)/comment', 'booktahoe.views.comment'),
    url(r'^(?P<night_id>\d+)/book', 'booktahoe.views.book'),
)