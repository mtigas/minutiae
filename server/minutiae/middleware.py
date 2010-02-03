from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib.sites.models import Site

class SuperuserSSLRedirect:
    def process_request(self, request):
        # Note this middleware allows the client to leak cookie data via HTTP, but at least it does not
        # allow the server to leak data back.
        
        # Only do this if the current user is a superuser.
        if request.user.is_authenticated() and request.user.is_superuser:
            if not self._is_secure(request):
                domain = Site.objects.get_current().domain
                newurl = "https://%s%s" % (domain,request.get_full_path())
                if settings.DEBUG and request.method == 'POST':
                    raise RuntimeError, \
                """Django can't perform a SSL redirect while maintaining POST data.
                   Please structure your views so that redirects only occur during GETs."""

                return HttpResponseRedirect(newurl)

    def _is_secure(self, request):
        if request.is_secure() or ('HTTP_X_FORWARDED_PROTOCOL' in request.META):
            return True
        
        #Handle the Webfaction case until this gets resolved in the request.is_secure()
        if 'HTTP_X_FORWARDED_SSL' in request.META:
            return request.META['HTTP_X_FORWARDED_SSL'] == 'on'

        return False
