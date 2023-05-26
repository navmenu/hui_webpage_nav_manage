# use the normal settings
from hui_webpage_nav_manage.settings import *

print("---------------")
print("settings_online")

DEBUG = False  # 注意这里是新增了个变量但由于恰好重名因此覆盖了老变量，其最终会影响到 django.conf.settings.DEBUG 的真假
LOGGING['root']['level'] = 'INFO'
# ELASTIC_APM['DEBUG'] = False

print("---------------")
