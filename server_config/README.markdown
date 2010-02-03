# Server configurations #

My server is deployed using [nginx][nginx] as the forward-facing server
that proxies connections to [Apache/mod_wsgi][apachewsgi], as necessary.

[nginx]: http://wiki.nginx.org/
[apachewsgi]: http://docs.djangoproject.com/en/dev/howto/deployment/modwsgi/

The files in this directory are _examples_ of server configuration files
and may differ *significantly* from my actual operating server configuration.

I've tried my best to comment out ambiguous sections of the configuration
for the benefit of those learning how to deploy Django+Apache/mod_wsgi behind nginx
(along with [nginx serving directly out of the django cache][nginxcache]).

[nginxcache]: http://weichhold.com/2008/09/12/django-nginx-memcached-the-dynamic-trio/

[Questions and comments are welcome.](http://mike.tig.as/contact/)
