"""
celery.py
--------------------------------------------------------------------
Add the celery app to the site and all the settings of celery are given here.
"""
import os
from django.conf import settings
from celery import Celery
from celery.schedules import crontab


# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'swLab.settings')

app = Celery('swLab')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object(settings, namespace='CELERY')

app.conf.beat_schedule={
	'webscrapper' : {
		'task' : 'jobHunt.tasks.periodic_update',
		'schedule' : crontab(hour=16, minute=24),
	}
}

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
