from django import template
import urllib, hashlib

register = template.Library()

@register.tag(name="gravatar")
def gravatar_for_email(parser, token):
    """
    Takes three arguments:
     * email variable
     * size
     * rating (g, pg, r, x)
     
    {% gravatar user.email 40 r %}
    """
    try:
        tag_name, email, size, rating = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires three arguments" % token.contents.split()[0]
    
    return GravatarNode(email, size, rating)

class GravatarNode(template.Node):
    def __init__(self, email, size, rating):
        self.email = email
        self.size = size
        self.rating = rating
    
    def render(self, context):
        email = template.resolve_variable(self.email, context).lower()
        size = self.size
        rating = self.rating
        
        gravatar_url = "https://secure.gravatar.com/avatar/%s.jpg?" % hashlib.md5(email).hexdigest()
        gravatar_url += urllib.urlencode({
            'd':'identicon',
            'size':str(size),
            'r':rating
        })
        return gravatar_url
