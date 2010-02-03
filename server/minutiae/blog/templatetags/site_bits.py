from django import template, get_version as get_django_version
register = template.Library()

from datetime import datetime
from minutiae.blog.models import BlogPost
from django.core.urlresolvers import reverse

@register.simple_tag
def current_django_version():
    return get_django_version()

@register.tag
def nav_footer(parser, token):
    return FooterNode()
    
class FooterNode(template.Node):
    def render(self, context):

        year_objects = get_valid_dates()

        left_link = None
        left_link_url = None
        right_link = None
        right_link_url = None
        
        try:
            page = template.Variable("page_obj.number").resolve(context)
        except:
            page = None
        try:
            post = template.Variable("post").resolve(context)
        except:
            post = None
        try:
            date_archive = template.Variable("date_archive").resolve(context)
        except:
            date_archive = None
            
        if page is not None:
            if page is 0:
                right_link = "Older"
                right_link_url = reverse("blog:archive",args=[1,])
            else:
                try:
                    has_previous = template.Variable("page_obj.has_previous").resolve(context)
                    previous_num = template.Variable("page_obj.previous_page_number").resolve(context)
                except:
                    has_previous = None
                try:
                    has_next = template.Variable("page_obj.has_next").resolve(context)
                    next_num = template.Variable("page_obj.next_page_number").resolve(context)
                except:
                    has_next = None
            
                if has_next:
                    right_link = "Older"
                    right_link_url = reverse("blog:archive",args=[next_num,])
                if has_previous:
                    left_link = "Newer"
                    left_link_url = reverse("blog:archive",args=[previous_num,])
        #elif post:
        #    try:
        #        older_post = post.get_previous_by_pubdate(is_live=True,pubdate__lte=datetime.now())
        #        right_link = older_post.title
        #        right_link_url = older_post.get_absolute_url()
        #    except:
        #        pass
        #    try:
        #        newer_post = post.get_next_by_pubdate(is_live=True,pubdate__lte=datetime.now())
        #        left_link = newer_post.title
        #        left_link_url = newer_post.get_absolute_url()
        #    except:
        #        pass
        elif date_archive is "year":
            try:
                year = int(template.Variable("year").resolve(context))
                if BlogPost.objects.filter(is_live=True,pubdate__year=year+1):
                    left_link = year+1
                    left_link_url = reverse("blog:archive_year",args=[year+1,])
                if BlogPost.objects.filter(is_live=True,pubdate__year=year-1):
                    right_link = year-1
                    right_link_url = reverse("blog:archive_year",args=[year-1,])
            except:
                pass
        elif date_archive is "month":
            try:
                month = template.Variable("month").resolve(context)
            except:
                month = None
            if month:
                try:
                    posts = template.Variable("object_list").resolve(context)
                except:
                    posts = None
                if posts:
                    try:
                        newer = posts[0].get_next_by_pubdate(is_live=True,pubdate__lte=datetime.now())
                        left_link = newer.pubdate.strftime("%B %Y")
                        left_link_url = reverse("blog:archive_month",args=[newer.pubdate.year,newer.pubdate_month])
                    except:
                        pass
                    try:
                        older = posts[-1].get_previous_by_pubdate(is_live=True,pubdate__lte=datetime.now())
                        right_link = older.pubdate.strftime("%B %Y")
                        right_link_url = reverse("blog:archive_month",args=[older.pubdate.year,older.pubdate_month])
                    except:
                        pass                                
        elif date_archive is "day":
            try:
                day = template.Variable("day").resolve(context)
            except:
                day = None
            if day:
                try:
                    posts = template.Variable("object_list").resolve(context)
                except:
                    posts = None
                if posts:
                    try:
                        newer = posts[0].get_next_by_pubdate(is_live=True,pubdate__lte=datetime.now())
                        left_link = newer.pubdate.strftime("%b. %d, %Y")
                        left_link_url = reverse("blog:archive_day",args=[newer.pubdate.year,newer.pubdate_month,newer.pubdate_day])
                    except:
                        pass
                    try:
                        older = posts[-1].get_previous_by_pubdate(is_live=True,pubdate__lte=datetime.now())
                        right_link = older.pubdate.strftime("%b. %d, %Y")
                        right_link_url = reverse("blog:archive_day",args=[older.pubdate.year,older.pubdate_month,older.pubdate_day])
                    except:
                        pass                                
        
        return template.loader.render_to_string(
            'blog/bits/nav_footer.html', {
                'year_objects':year_objects,
                'left_link':left_link,
                'left_link_url':left_link_url,
                'right_link':right_link,
                'right_link_url':right_link_url
        })






# Helpers

def get_valid_dates():
    valid_months = []
    valid_years = []

    for pubdate in BlogPost.objects.filter(is_live=True,pubdate__lte=datetime.now()).values_list('pubdate',flat=True):
        m = pubdate.date().replace(day=1)
        y = pubdate.date().replace(day=1,month=1)

        if not m in valid_months:
            valid_months.append(m)
        if not y in valid_years:
            valid_years.append(y)

    year_objects = { }
    for y in valid_years:
        year_objects[y.year] = Year(y.year)

    for m in valid_months:
        year_objects[m.year].activate_month(m.month)

    real_year_objects = year_objects.items()
    real_year_objects.sort()
    real_year_objects.reverse()

    return real_year_objects


class Year:
    def __init__(self,year):
        self.year = int(year)
        self.date_obj = datetime(year,1,1)
        self.months = []

        for i in range(1,13):
            self.months.append({
                'num':i,
                'date_obj':datetime(year,i,1),
                'is_active':False
            })

    def __eq__(self,other):
        if type(other) == type(self):
            return (self.year == other.year)
        elif type(other) == int:
            return (self.year == other)
        else:
            return False

    def __ne__(self,other):
        return not self.__eq__(other)

    def __lt__(self,other):
        if type(other) == type(self):
            return (self.year < other.year)
        elif type(other) == int:
            return (self.year < other)
        else:
            return NotImplemented

    def __le__(self,other):
        return self.__lt__(other) or self.__eq__(other)

    def __gt__(self,other):
        if type(other) == type(self):
            return (self.year > other.year)
        elif type(other) == int:
            return (self.year > other)
        else:
            return NotImplemented

    def __ge__(self,other):
        return self.__gt__(other) or self.__eq__(other)

    def __str__(self):
        return "%d" % self.year

    def __repr__(self):
        return "Year(%d)" % self.year

    def activate_month(self,monthnum):
        self.months[monthnum-1]['is_active'] = True
