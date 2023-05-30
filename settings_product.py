# use the normal settings
from hui_webpage_nav_manage.settings import *

print("---------------")
print("settings_online")

DEBUG = False  # 注意这里是新增了个变量但由于恰好重名因此覆盖了老变量，其最终会影响到 django.conf.settings.DEBUG 的真假
LOGGING['root']['level'] = 'INFO'
# ELASTIC_APM['DEBUG'] = False
ALLOWED_HOSTS = ['*']

BACKEND_API_PREFIX = "http://127.0.0.1:38000/api/web-navigation/v1/"
BACKEND_ANONYMOUS_TOKEN = "abc"  # 在没有登陆时，还是需要个token和服务器交互的

print("---------------")
