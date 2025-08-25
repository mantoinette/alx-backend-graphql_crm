#!/bin/bash
# Delete customers with no orders in the last year (or never ordered)
# Logs count to /tmp/customer_cleanup_log.txt

set -euo pipefail

PROJECT_DIR="/path/to/alx_backend_graphql_crm"   # <<< CHANGE THIS
PYTHON_BIN="$PROJECT_DIR/venv/bin/python"        # <<< CHANGE if not using venv
MANAGE="$PROJECT_DIR/manage.py"
LOG_FILE="/tmp/customer_cleanup_log.txt"

TIMESTAMP="$(date '+%Y-%m-%d %H:%M:%S')"

$PYTHON_BIN "$MANAGE" shell -c "
from datetime import datetime, timedelta, timezone
from crm.models import Customer
one_year_ago = datetime.now(timezone.utc) - timedelta(days=365)
to_delete = Customer.objects.exclude(orders__order_date__gte=one_year_ago)
count = to_delete.count()
to_delete.delete()
print(count)
" | {
  read COUNT
  echo \"$TIMESTAMP - Deleted $COUNT inactive customers\" >> \"$LOG_FILE\"
}
