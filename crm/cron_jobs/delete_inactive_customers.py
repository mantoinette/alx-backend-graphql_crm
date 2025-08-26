from datetime import datetime, timedelta
import os
import django

# Setup Django environment manually (adjust to your project settings)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crm.settings")  # change if your settings module is different
django.setup()

from crm.models import Customer, Order  # adjust import if your models path is different

# Delete customers with no orders in the last year
one_year_ago = datetime.now() - timedelta(days=365)
inactive_customers = Customer.objects.filter(order__created_at__lt=one_year_ago).distinct()
count = inactive_customers.count()
inactive_customers.delete()

# Log the result
with open("/tmp/customer_cleanup_log.txt", "a") as log_file:
    log_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Deleted {count} inactive customers\n")
