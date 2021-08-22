# Register your new serializer methods into kombu
from kombu.serialization import register
from .myjson import my_dumps, my_loads

register('myjson', my_dumps, my_loads, 
    content_type='application/x-myjson',
    content_encoding='utf-8') 

# Tell celery to use your new serializer:
CELERY_ACCEPT_CONTENT = ['myjson']
CELERY_TASK_SERIALIZER = 'myjson'
CELERY_RESULT_SERIALIZER = 'myjson'

BROKER_URL = 'redis://127.0.0.1:6379'               # 指定 Broker  
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'  # 指定 Backend  

CELERY_TIMEZONE='Asia/Shanghai'                     # 指定时区，默认是 UTC  
# CELERY_TIMEZONE='UTC'                               

CELERY_IMPORTS = (                                  # 指定导入的任务模块  
    'Malicious_app.classifier',
)


