from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.contrib.comments.moderation import CommentModerator, moderator

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
    
    title = models.CharField(max_length=255,blank=True)
    description = models.CharField(max_length=255,blank=True)
    slug = models.CharField(max_length=255)
    body = models.TextField()
    pubdate = models.DateTimeField(default=datetime.now)
    is_live = models.BooleanField(default=False)
    enable_comments = models.BooleanField(default=False)
    
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
        
        return "https://"+current_site.domain+reverse(
            'blog:post',
            kwargs = {
                'year' : self.pubdate.year,
                'month': self.pubdate.strftime('%m'),
                'day'  : self.pubdate.strftime('%d'),
                'slug' : self.slug
            })


class BlogCommentModerator(CommentModerator):
    email_notification = True
    enable_field = 'enable_comments'
    
    def check_spam(self, request, comment, key, blog_url=None, base_url=None):
        try:
            from akismet import Akismet
        except:
            return False
        
        if blog_url is None:
            blog_url = 'https://%s/' % Site.objects.get_current().domain
        
        ak = Akismet(
            key=settings.AKISMET_API_KEY,
            blog_url=blog_url
        )
        
        if base_url is not None:
            ak.baseurl = base_url
                
        if ak.verify_key():
            data = {
                'user_ip': request.META.get('REMOTE_ADDR', '127.0.0.1'),
                'user_agent': request.META.get('HTTP_USER_AGENT', ''),
                'referrer': request.META.get('HTTP_REFERER', ''),
                'comment_type': 'comment',
                'comment_author': comment.user_name.encode('utf-8'),
                'comment_author_email': comment.userinfo['email'],
                'comment_author_url': comment.userinfo['url']
            }
            
            if ak.comment_check(comment.comment.encode('utf-8'), data=data, build_data=True):
                return True
        return False
    
    def moderate(self, comment, content_object, request):
        moderate = super(BlogCommentModerator, self).moderate(comment, content_object, request)
                
        return moderate or self.check_spam(request, comment,
            key=settings.AKISMET_API_KEY,
        )

moderator.register(BlogPost, BlogCommentModerator)
