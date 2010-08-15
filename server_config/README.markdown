# Server configurations #

My server is deployed using [nginx][nginx] as the forward-facing server
that proxies connections to [uWSGI][uwsgi], which handles the actual
Python/Django application instance.

[nginx]: http://wiki.nginx.org/
[uwsgi]: http://projects.unbit.it/uwsgi/

The files in this directory are _examples_ of server configuration files
and may differ *significantly* from my actual operating server configuration.

I've tried my best to comment out ambiguous sections of the configuration
for the benefit of those learning how to deploy uWSGI behind nginx.

[Questions and comments are welcome.](https://mike.tig.as/contact/)

## Notes ##

The uWSGI instance is started as a daemon via an [upstart][upstart] script.
Those using other or older Linux distributions (which use the System-V init.d system),
will need to write their own init scripts to start this background server.

[upstart]: http://upstart.ubuntu.com/

You may have issues with socket permissions between nginx and uWSGI if the
socket directory doesn't allow read/write access to the nginx and uWSGI
daemon users (normally www-data).
