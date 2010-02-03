from defaults import *

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)


try:
    from secret_settings import *
except:
    pass
