#!/bin/bash

# Navigate to Django project root
cd /c/Users/anton/Documents/alx-backend-graphql_crm || exit

# Run Django shell command to delete inactive customers
DELETED_COUNT=$(python manage.py shell -c "
from datetime import datetime, timedelta
from crm.models import Customer, Order

one_year_ago = datetime.now() - timedelta(days=365)
inactive_customers = Customer.objects.filter(order__created_at__lt=one_year_ago).distinct()
count = inactive_customers.count()
inactive_customers.delete()
print(count)
")

# Log the number of deleted customers
echo \"\$(date '+%Y-%m-%d %H:%M:%S') - Deleted \$DELETED_COUNT inactive customers\" >> /tmp/customer_cleanup_log.txt
