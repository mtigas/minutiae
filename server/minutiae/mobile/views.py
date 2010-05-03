from django.db.models.loading import get_model
from django.http import HttpResponse
from models import SECTIONS_ORDER,SECTIONS
try:
    import json
except ImportError:
    import simplejson as json

def sections(request):
    data = []
    for order,slug in enumerate(SECTIONS_ORDER):
        section = SECTIONS[slug]
        
        data.append({
            'order':int(order),
            'slug':unicode(section['slug']),
            'name':unicode(section['name'])
        })
    
    response = HttpResponse(
        content=json.dumps(
            data,
            ensure_ascii=False,
            indent=2),
        mimetype="text/plain;charset=utf-8"
    )
    
    from django.db import connection
    print connection.queries
    
    return response

def section_detail(request,slug=''):
    if not SECTIONS.has_key(slug):
        return HttpResponse(
            u"{}",
            mimetype="text/plain;charset=utf-8"
        )
    
    section = SECTIONS[slug]
    
    data = {
        'slug':section['slug'],
        'name':section['name']
    }
    
    Model = get_model('mobile',section['proxy_model'])
    
    items = []
    for m in Model.objects.all():
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
            indent=2),
        mimetype="text/plain;charset=utf-8"
    )
    
    from django.db import connection
    print connection.queries
    
    return response
