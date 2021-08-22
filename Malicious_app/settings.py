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
