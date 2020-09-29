import os  
from celery import Celery #pip install celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agregator.settings')
celery_app = Celery('agregator')  
celery_app.config_from_object('django.conf:settings', namespace='CELERY')  
celery_app.autodiscover_tasks()

@celery_app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request)) 
