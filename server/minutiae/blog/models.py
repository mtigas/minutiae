from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from datetime import datetime

class PostCategory(models.Model):
    objects = models.Manager()
    
    name = models.CharField(max_length=255)
    plural = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = 'post categories'

    def __unicode__(self):
        return u'%s' % self.name

class BlogPost(models.Model):
    objects = models.Manager()
    
    post_type = models.ForeignKey(PostCategory,default=1)
    
    title   = models.CharField(max_length=255,blank=True)
    slug    = models.CharField(max_length=255)
    body    = models.TextField()
    pubdate = models.DateTimeField(default=datetime.now)
    is_live = models.BooleanField(default=False)
    
    class Meta:
        get_latest_by = 'pubdate'
        ordering = ['-pubdate','title']
        unique_together = (('pubdate','slug'),)
    
    def __unicode__(self):
        return u'%s' % self.title
    
    @property
    def pubdate_month(self):
        if self.pubdate.month < 10:
            return "0%s" % self.pubdate.month
        else:
            return self.pubdate.month

    @property
    def pubdate_day(self):
        if self.pubdate.day < 10:
            return "0%s" % self.pubdate.day
        else:
            return self.pubdate.day
    
    @models.permalink
    def get_absolute_url(self):
        return ('blog:post', (), {
            'year' : self.pubdate.year,
            'month': self.pubdate.strftime('%m'),
            'day'  : self.pubdate.strftime('%d'),
            'slug' : self.slug
        })
    
    def absolute_uri(self):
        current_site = Site.objects.get_current()
        
        return "http://"+current_site.domain+reverse(
            'blog:post',
            kwargs = {
                'year' : self.pubdate.year,
                'month': self.pubdate.strftime('%m'),
                'day'  : self.pubdate.strftime('%d'),
                'slug' : self.slug
            })
