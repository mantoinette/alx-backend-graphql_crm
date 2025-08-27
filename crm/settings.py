INSTALLED_APPS = [
    # ... your other apps ...
    'django_crontab',
]
CRONJOBS = [
    ('*/12* * * *', 'crm.cron.log_crm_heartbeat'),
]
