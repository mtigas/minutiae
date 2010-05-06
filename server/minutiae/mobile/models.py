from django.db import models
from minutiae.blog.models import BlogPost
from datetime import datetime

class MobileBlogPost(BlogPost):
    class Meta:
        proxy = True
    
    def get_mobile_text(self):
        return self.body
    
    def get_mobile_photos(self):
        return None
    
    def get_mobile_videos(self):
        return None
        
    def get_mobile_teaser_text(self):
        return self.body
    
    def get_mobile_teaser_photo(self):
        return None
    
    def get_mobile_teaser_video(self):
        return None


SECTIONS_ORDER = (
    'main',
)
SECTIONS = {
    'main': {
        'slug':'main',
        'name':'Main Content',
        'filters':{
            'is_live__exact':True,
            'pubdate__lte':datetime.now
        },
        'excludes':{},
        'proxy_model':MobileBlogPost
    },
}
