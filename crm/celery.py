# crm/celery.py
import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crm.settings")

app = Celery("crm")
# Read config from Django settings with keys prefixed by CELERY_
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks in installed apps (looks for tasks.py)
app.autodiscover_tasks()
