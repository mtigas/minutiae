from django.conf.urls.defaults import *
import views

urlpatterns = patterns('',
    url(
        regex = r'^$',
        view = views.sections,
        name = 'sections'
    ),
    url(
        regex = r'^(?P<slug>[-\w]+)/$',
        view = views.section_detail,
        name = 'section_detail'
    )
)