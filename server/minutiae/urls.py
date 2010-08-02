from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from minutiae.blog.feeds import BlogFeed
from minutiae.sitemaps import server_sitemaps
from minutiae.custom_contact_form import CustomRecipientContactForm

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$',
        'django.views.generic.simple.direct_to_template', {
            'template': 'index.html'
        }
    ),
    
    # Blog & blog shorturl
    (r'^blog/', include('minutiae.blog.urls', namespace="blog", app_name="blog")),
    #(r'^b/(?P<post_id>\d+)/$', 'minutiae.blog.views.short_redir'),
    
    # Blog & blog shorturl
    (r'^_test/', include('minutiae.mobile.urls', namespace="mobile", app_name="mobile")),
    
    # Some fake flatpages
    (r'^about/$', 'django.views.generic.simple.direct_to_template', { 'template':'about.html' }),
    (r'^colophon/$', 'django.views.generic.simple.direct_to_template', { 'template':'colophon.html' }),
    (r'^portfolio/$', 'django.views.generic.simple.direct_to_template', { 'template':'portfolio.html' }),
    
    # Comments backend
    url(r'^comments/cr/(\d+)/(.+)/$', 'minutiae.views.shortcut', name='comments-url-redirect'),
    (r'^comments/', include('django.contrib.comments.urls')),
    
    # Feed framework
    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': {
        'blog':BlogFeed
    }}),
    
    # Sitemaps framework
    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': server_sitemaps}),
    
    # django-contact-form
    url(r'^contact/$',
        'contact_form.views.contact_form', {
            'form_class':CustomRecipientContactForm
        },
        name='contact_form'),
    url(r'^contact/sent/$',
        'django.views.generic.simple.direct_to_template', {
            'template': 'contact_form/contact_form_sent.html'
        },
        name='contact_form_sent'),
    
    # Admin
    (r'^__mtadmin_/', include(admin.site.urls)),
)

if settings.DEBUG:
    from os.path import join as path_join

    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$',
            'django.views.static.serve', {
                'document_root': settings.MEDIA_ROOT,
                'show_indexes': True
        }),
        (r'^admin_media/(?P<path>.*)$',
            'django.views.static.serve', {
                'document_root': path_join(
                    settings.DJANGO_SERVER_DIR,
                    'third_party',
                    'django','contrib','admin','media'
                ),
                'show_indexes': True
        }),
    )
