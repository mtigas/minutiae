from django.contrib.syndication.feeds import Feed
from models import BlogPost
from datetime import datetime
from django.utils import feedgenerator

class BlogFeed(Feed):
    feed_type = feedgenerator.Atom1Feed
    
    title = "Minutiae by Mike Tigas"
    link = "http://mike.tig.as/blog/"
    description = "Loud thinking from the mind of Mike Tigas."

    def items(self):
        return BlogPost.objects.filter(is_live=True,pubdate__lte=datetime.now()).order_by('-pubdate')[:15]
    
    def copyright(self):
        return 'Copyright &#169; 2001-%s, Mike Tigas (see http://mike.tig.as/colophon/#license)' % datetime.now().year
    author_link = "http://mike.tig.as/about/"
    author_name = "Mike Tigas"
    
    def item_pubdate(self,item):
        return item.pubdate

    def item_copyright(self,obj):
        return 'Copyright &#169; %s, Mike Tigas (see http://mike.tig.as/colophon/#license)' % obj.pubdate.year
    
    title_template       = "feeds/blog_title.html"
    description_template = "feeds/blog_description.html"
