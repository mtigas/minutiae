from django.db.models.loading import get_model
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse,NoReverseMatch
from django.views.generic.simple import redirect_to

from models import SECTIONS_ORDER,SECTIONS
try:
    import json
except ImportError:
    import simplejson as json

def sections(request):
    data = []
    for order,slug in enumerate(SECTIONS_ORDER):
        section = SECTIONS[slug]
        
        Model = get_model('mobile',section['proxy_model'])
        qs = Model._default_manager.all()
        print section['filters']
        if section['filters']:
            qs = qs.filter(**section['filters'])
        if section['excludes']:
            qs = qs.exclude(**section['excludes'])
        
        p = Paginator(qs,20)
        
        data.append({
            'order':int(order),
            'slug':unicode(section['slug']),
            'name':unicode(section['name']),
            'num_items':int(p.count),
            'num_pages':int(p.num_pages),
            'page_range':p.page_range,
        })
    
    response = HttpResponse(
        content=json.dumps(
            data,
            ensure_ascii=False,
            #indent=2,
        ),
        mimetype="text/plain;charset=utf-8"
    )
    
    from django.db import connection
    print "%s queries" % len(connection.queries)
    
    return response

def section_detail_redir(request,slug=''):
    if not SECTIONS.has_key(slug):
        return HttpResponse(
            u"{}",
            mimetype="text/plain;charset=utf-8",
            status=400
        )
    
    try:
        url = reverse("mobile:section_detail",args=[slug,1])
        return redirect_to(
            request,
            url
        )
    except NoReverseMatch:
        return HttpResponse(
            u"{}",
            mimetype="text/plain;charset=utf-8",
            status=400
        )

def section_detail(request,slug='',page=1):
    if not SECTIONS.has_key(slug):
        return HttpResponse(
            u"{}",
            mimetype="text/plain;charset=utf-8",
            status=400
        )
    
    section = SECTIONS[slug]
    
    Model = get_model('mobile',section['proxy_model'])
    qs = Model._default_manager.all()
    if section['filters']:
        qs = qs.filter(**section['filters'])
    if section['excludes']:
        qs = qs.exclude(**section['excludes'])
    
    p = Paginator(qs,20)
    
    data = {
        'slug':section['slug'],
        'name':section['name'],
        'num_items':int(p.count),
        'num_pages':int(p.num_pages),
        'page_range':p.page_range,
    }
    
    items = []
    for m in qs:
        items.append({
            'id':int(m.pk),
            'title':unicode(m),
            'content':unicode(m.get_mobile_text()),
            'pubdate':unicode(m.pubdate)
        })
    
    data['items'] = items
    
    response = HttpResponse(
        content=json.dumps(
            data,
            ensure_ascii=False,
            indent=2,
        ),
        mimetype="text/plain;charset=utf-8"
    )
    
    #from django.db import connection
    #print "%s queries" % len(connection.queries)
    
    return response
