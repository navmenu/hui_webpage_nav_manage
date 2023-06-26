"""
URL configuration for hui_webpage_nav_manage project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView

import nav_manage.views
from utils.utils_static import static_urlpatterns, static_urlpattern

urlpatterns = [
    path('', nav_manage.views.index),
    path('admin/', admin.site.urls),
    path("nav_manage/", include("nav_manage.urls")),
]

# 以下代码主要是解决了在 DEBUG = False 时网页不能加载静态文件的问题
# 有一种思路是这样的，显然它和官方推荐的 django.conf.urls.static 策略是相同的，它也是可运行的，我们仿照官方改就行
# urlpatterns = [
#     re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
#     re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
# ]
if not settings.DEBUG:  # 这里使用+也行，使用扩展也行，相当于非开发环境的静态资源
    urlpatterns.extend(static_urlpatterns(settings.STATIC_URL, document_root=settings.STATIC_ROOT))
    urlpatterns.extend(static_urlpatterns(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))

# 以下代码主要是解决 "GET /favicon.ico HTTP/1.1" 404 获得网站图标的问题，假如不设置图标则有一个小的告警，因此需要添加个图标
if not settings.DEBUG:
    # 这个方法是比较标准的，在测试环境我们使用RedirectView重定向，其实这里也能用重定向的方式解决，但多学习一种方式也挺好的，我们也可以在测试环境直接指定文件，但静态文件的位置和线上是不同的
    urlpatterns.append(static_urlpattern('favicon.ico', document_root=settings.STATIC_ROOT, document_path='hui_webpage_nav_manage/mysite_favicon_128x128.ico'))
else:
    # 这种方案是使用 from django.urls import re_path 的，它的作用和直接使用 path 是完全相同的
    # urlpatterns.append(re_path(r'^favicon\.ico$', RedirectView.as_view(url=r'static/hui_webpage_nav_manage/mysite_favicon.ico')))
    # 其实测试和线上我们都可以用重定向这一种方式解决，这样一行代码即可解决问题，但毕竟多学习一种方式也是极好的，因此我们分开写两种情况
    urlpatterns.append(path('favicon.ico', RedirectView.as_view(url=r'static/hui_webpage_nav_manage/mysite_favicon.ico')))
