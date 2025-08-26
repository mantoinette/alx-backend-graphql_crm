# delete_inactive_customers.py
import os
import django
from datetime import datetime, timedelta

# Replace 'crm.settings' with your actual Django settings module path
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crm.settings")
django.setup()

from yourapp.models import Customer, Order  # replace 'yourapp' with your app name

one_year_ago = datetime.now() - timedelta(days=365)

# Delete customers with no orders in the past year
inactive_customers = Customer.objects.filter(order__date__lt=one_year_ago)
deleted_count, _ = inactive_customers.delete()

print(f"Deleted {deleted_count} inactive customers.")
