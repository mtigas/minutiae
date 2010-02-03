from django.conf.urls.defaults import *
import views

urlpatterns = patterns('',
    url(
        regex = r'^$',
        view = views.index,
        name = 'home'
    ),
    url(
        regex = r'^archive/$',
        view = views.archive_redirector
    ),
    url(
        regex = r'^archive/(?P<page>\d+)/$',
        view = views.archive,
        name = 'archive'
    ),
    url(
        regex = r'^(?P<year>\d{4})/$',
        view = views.archive_year,
        name = 'archive_year'
    ),
    url(
        regex = r'^(?P<year>\d{4})/(?P<month>\d{1,2})/$',
        view = views.archive_month,
        name = 'archive_month'
    ),
    url(
        regex = r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$',
        view = views.archive_day,
        name = 'archive_day'
    ),
    url(
        regex = r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/$',
        view = views.post,
        name = 'post'
    ),
    url(
        regex = r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/json/$',
        view = views.post_json,
        name = 'post_json'
    )
)
