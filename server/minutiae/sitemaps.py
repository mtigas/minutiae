from django.contrib.sitemaps import Sitemap, GenericSitemap
from datetime import datetime
from minutiae.blog.models import BlogPost

class StaticFilesSitemap(Sitemap):
    def items(self):
        return [
        {
            'url':'/',
            'priority':1,
            'lastmod':BlogPost.objects.filter(is_live=True,pubdate__lte=datetime.now()).latest().pubdate,
            'changefreq':'always',
        }, {
            'url':'/about/',
            'priority':.9,
            'lastmod':datetime(2010,01,30,03),
            'changefreq':'weekly'
        }, {
            'url':'/portfolio/',
            'priority':.9,
            'lastmod':datetime(2010,01,30,03),
            'changefreq':'weekly'
        }, {
            'url':'/colophon/',
            'priority':.8,
            'lastmod':datetime(2010,01,30,03),
            'changefreq':'weekly'
        }   
    ]
    def location(self,item):
        return item['url']
    
    def lastmod(self,item):
        return item['lastmod']
    
    def changefreq(self,item):
        return item['changefreq']
    
    def priority(self,item):
        return item['priority']

server_sitemaps = {
    'statics':StaticFilesSitemap,
    'blog':GenericSitemap({
        'queryset':BlogPost.objects.filter(is_live=True,pubdate__lte=datetime.now()),
        'date_field': 'pubdate'
    }, priority=.8)
}
