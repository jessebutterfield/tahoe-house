from django.conf.urls import patterns, url

urlpatterns = patterns('',
    # ex: /nights/5/
    url(r"^(\d+)/(\d+)/(\d+)/$", 'booktahoe.views.detail'),
    url(r"^(\d+)/(\d+)/(\d+)/(\d+)/$", 'booktahoe.views.detail'),
    url(r"^(\d+)/(\d+)/(prev|next)$", 'booktahoe.views.newMonth'),
    url(r"^(\d+)/(\d+)/$", 'booktahoe.views.month'),
    url(r'^(?P<night_id>\d+)/comment', 'booktahoe.views.comment'),
    url(r'^editComment/(?P<comment_id>\d+)', 'booktahoe.views.editComment'),
    url(r'^(?P<night_id>\d+)/book', 'booktahoe.views.book'),
    url(r'^(?P<comment_id>\d+)/deleteComment', 'booktahoe.views.deleteComment'),
    url(r'^userUpdate/$', 'booktahoe.views.updateInfo'),
    url(r'^saveInfo', 'booktahoe.views.saveInfo'),
    url(r'^login/$', 'django.contrib.auth.views.login', {
    'template_name': 'nights/login.html'}),
    url(r'^postLogin/', 'booktahoe.views.postLogin'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
                          {'next_page': '/'}),
    url(r'^$', 'booktahoe.views.currentMonth'),
)