from django.http import HttpResponse
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse,NoReverseMatch
from django.views.generic.simple import redirect_to

from models import SECTIONS_ORDER,SECTIONS
try:
    import json
except ImportError:
    import simplejson as json

JSON_404 = HttpResponse(
    u"{}",
    mimetype="text/plain;charset=utf-8",
    status=404
)

def sections(request):
    data = []
    for order,slug in enumerate(SECTIONS_ORDER):
        section = SECTIONS[slug]
        
        Model = section['proxy_model']
        qs = Model._default_manager.all()
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
        })
    
    response = HttpResponse(
        content=json.dumps(
            data,
            ensure_ascii=False,
            #indent=2,
        ),
        mimetype="text/plain;charset=utf-8"
    )
    
    #from django.db import connection
    #print "%s queries" % len(connection.queries)
    
    return response

def section_detail_redir(request,slug=''):
    if not SECTIONS.has_key(slug):
        return JSON_404
    
    try:
        url = reverse("mobile:section_detail",args=[slug,1])
        return redirect_to(
            request,
            url
        )
    except NoReverseMatch:
        return JSON_404

def section_detail(request,slug='',page_num=1):
    if not (SECTIONS.has_key(slug) and page_num.isdigit()):
        return JSON_404
    
    page_num = int(page_num)
    
    section = SECTIONS[slug]
    
    Model = section['proxy_model']
    qs = Model._default_manager.all()
    if section['filters']:
        qs = qs.filter(**section['filters'])
    if section['excludes']:
        qs = qs.exclude(**section['excludes'])
    
    p = Paginator(qs,20)
    if page_num not in p.page_range:
        return JSON_404
    
    page = p.page(page_num)
    
    if page.has_next():
        next_page = page.next_page_number()
    else:
        next_page = -1
    
    if page.has_previous():
        previous_page = page.previous_page_number()
    else:
        previous_page = -1
    
    data = {
        'slug':section['slug'],
        'name':section['name'],
        'num_items':int(p.count),
        'num_pages':int(p.num_pages),
        'next_page':next_page,
        'previous_page':previous_page,
    }
    
    items = []
    for m in p.object_list:
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
