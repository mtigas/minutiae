from django.views.generic import date_based,list_detail
from django.views.generic.simple import direct_to_template,redirect_to
from django.http import HttpResponse,Http404
from django.core import serializers
from django.core.urlresolvers import reverse,NoReverseMatch
from django.conf import settings
from models import BlogPost
import hashlib
from datetime import datetime,date

def double_digit_checker(request,year,month,day=None):
    if len(month) == 1:
        try:
            url = reverse(
                "blog:archive_month",
                args=[year,"0%s" % month]
            )
        except:
            raise Http404
        return redirect_to(
            request,
            url
        )
    if day and len(day) == 1:
        try:
            url = reverse(
                "blog:archive_month",
                args=[year,month,"0%s" % day]
            )
        except:
            raise Http404
        return redirect_to(
            request,
            url
        )
    return None

def home_redirector(request):
    try:
        url = reverse("blog:home")
        return redirect_to(
            request,
            url
        )
    except:
        raise Http404

def archive_redirector(request):
    try:
        url = reverse("blog:archive",[1])
        return redirect_to(
            request,
            url
        )
    except:
        raise Http404

def index(request):
    return date_based.archive_index(
        request,
        queryset   = BlogPost.objects.filter(is_live=True),
        date_field = 'pubdate',
        num_latest = 5,
        template_name = 'blog/index.html',
        template_object_name = 'object_list',
        extra_context = {
            'page_obj':{'number':0}
        }
    )

def archive(request,page=None):
    if not page:
        page = 1
    if (int(page) is 1):
        url = reverse("blog:home")
        return redirect_to(
            request,
            url,
            permanent=False
        )
    return list_detail.object_list(
        request,
        queryset   = BlogPost.objects.filter(is_live=True),
        paginate_by = 5,
        page = page,
        template_name = 'blog/index.html',
        template_object_name = 'object'
    )

def short_redir(request,post_id):
    try:
        post = BlogPost.objects.filter(is_live=True).get(pk=post_id)
    except BlogPost.DoesNotExist:
        raise Http404
    
    return redirect_to(
        request,
        post.get_absolute_url()
    )

def post(request,year,month,day,slug):
    redirect = double_digit_checker(request,year,month,day)
    if redirect:
        return redirect
    
    try:
        d = date(int(year),int(month),int(day))
    except:
        raise Http404

    # Generate a preview code -- lets admin distribute a URL to nonprivieged users
    # to view non-published posts.
    preview_code = hashlib.sha512("%s%s%s%s%s%s"%(
        datetime.now().strftime("%Y%U"), # expire code based on week
        year,
        month,
        day,
        slug,
        settings.SECRET_KEY
    )).hexdigest()
    preview_code = hashlib.sha512("%s%s%s%s%s%s"%(preview_code,year,month,day,slug,settings.SECRET_KEY)).hexdigest()
    preview_code = hashlib.md5(preview_code+settings.SECRET_KEY).hexdigest()
    
    if request.user.is_authenticated() and request.user.is_superuser:
        # Superusers can view posts that are not yet live (so admin's "view on site" works to preview)
        qs = BlogPost.objects.all()
    elif 'code' in request.GET:
        # If we match the preview code, show any article regardless of publish status and date.
        if preview_code == request.GET['code']:
            qs = BlogPost.objects.all()
        else:
            qs = BlogPost.objects.filter(is_live=True,pubdate__lte=datetime.now())
    else:
        qs = BlogPost.objects.filter(is_live=True,pubdate__lte=datetime.now())
    
    return date_based.object_detail(
        request,
        year = year,
        month = month,
        month_format = "%m",
        day = day,
        queryset = qs,
        slug = slug,
        slug_field = 'slug',
        date_field = 'pubdate',
        template_name = 'blog/post_detail.html',
        template_object_name = 'post',
        extra_context = dict(
            preview_code=preview_code,
            request=request
        )
    )

def post_json(request,year,month,day,slug):
    redirect = double_digit_checker(request,year,month,day)
    if redirect:
        return redirect
    
    try:
        d_min = datetime(int(year),int(month),int(day),0,0,0)
        d_max = d_min.replace(hour=23,minute=59,second=59)
    except:
        raise Http404
    
    qs = BlogPost.objects.filter(
        is_live=True,
        pubdate__gte=d_min,
        pubdate__lte=d_max,
        slug=slug
    )
    response = HttpResponse(
        content_type="application/json"
    )
    json_serializer = serializers.get_serializer("json")()
    json_serializer.serialize(qs, ensure_ascii=False, stream=response)

    return response

def archive_year(request,year):
    qs = BlogPost.objects.filter(is_live=True,pubdate__year=year)
    if qs:
        pass
    return date_based.archive_year(
        request,
        year = year,
        queryset   = BlogPost.objects.filter(is_live=True),
        date_field = 'pubdate',
        #template_name = 'blog/date_archive_abbr.html',
        template_name = 'blog/date_archive.html',
        make_object_list = True,
        template_object_name = 'object',
        extra_context = {
            'title' : "%s" % year,
            'date_archive' : 'year'
        }
    )

def archive_month(request,year,month):
    redirect = double_digit_checker(request,year,month)
    if redirect:
        return redirect

    try:
        d = date(int(year),int(month),1)
    except:
        raise Http404

    return date_based.archive_month(
        request,
        year = year,
        month = month,
        month_format = "%m",
        queryset   = BlogPost.objects.filter(is_live=True),
        date_field = 'pubdate',
        #template_name = 'blog/date_archive_abbr.html',
        template_name = 'blog/date_archive.html',
        extra_context = {
            'title' : d.strftime("%B %Y"),
            'date_archive' : 'month'
        }
    )

def archive_day(request,year,month,day):
    redirect = double_digit_checker(request,year,month,day)
    if redirect:
        return redirect
    
    try:
        d = date(int(year),int(month),int(day))
    except:
        raise Http404
    
    return date_based.archive_day(
        request,
        year = year,
        month = month,
        month_format = "%m",
        day = day,
        queryset   = BlogPost.objects.filter(is_live=True),
        date_field = 'pubdate',
        template_name = 'blog/date_archive.html',
        extra_context = {
            'title' : d.strftime("%b. %d, %Y"),
            'date_archive' : 'day'
        }
    )
