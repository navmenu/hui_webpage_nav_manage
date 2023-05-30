import re

from django.conf import settings
from django.urls import path, re_path
from django.views.static import serve


# 代码仿照 django.conf.urls.static . 但是有个改动就是它的代码是 not DEBUG 时返回空[]，而我的是DEBUG时返回空
def static_urlpatterns(prefix, view=serve, **kwargs):
    if settings.DEBUG:
        return []
    return [re_path(r"^%s(?P<path>.*)$" % re.escape(prefix.lstrip("/")), view, kwargs=kwargs)]


def static_urlpattern(urlpath, document_root, document_path):
    return path(urlpath, serve, {'document_root': document_root, 'path': document_path})
