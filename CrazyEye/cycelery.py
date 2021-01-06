import os
from celery import Celery
from django.conf import settings


project_name = os.path.split(os.path.abspath('.'))[-1]

project_settings = '%s.settings' %(project_name)


#config env
os.environ.setdefault('DJANGO_SETTINGS_MODULE',project_settings)

#instantiation celery
app = Celery(project_name)

#use django config settings
app.config_from_object('django.conf:settings')

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))