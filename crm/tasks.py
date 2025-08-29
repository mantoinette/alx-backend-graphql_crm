# crm/tasks.py
from celery import shared_task
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from datetime import datetime
import os
import requests

GRAPHQL_URL = os.environ.get("GRAPHQL_URL", "http://localhost:8000/graphql/")
LOG_FILE = os.environ.get("CRM_REPORT_LOG", "/tmp/crm_report_log.txt")

@shared_task
def generate_crm_report():
    """
    Queries the GraphQL endpoint for total customers, total orders and total revenue,
    then logs to /tmp/crm_report_log.txt with timestamp:
    YYYY-MM-DD HH:MM:SS - Report: X customers, Y orders, Z revenue
    """
    transport = RequestsHTTPTransport(
        url=GRAPHQL_URL,
        verify=True,
        retries=3,
    )

    client = Client(transport=transport, fetch_schema_from_transport=False)

    # Example GraphQL query — adjust if your schema uses different field names
    query = gql("""
    query {
      crmReport {
        totalCustomers
        totalOrders
        totalRevenue
      }
    }
    """)

    # default values in case query fails or fields missing
    customers = orders = revenue = 0
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        resp = client.execute(query)
        # resp can be like {"crmReport": {"totalCustomers": 1, ...}}
        report = resp.get("crmReport", resp)
        customers = report.get("totalCustomers", report.get("total_customers", 0))
        orders = report.get("totalOrders", report.get("total_orders", 0))
        revenue = report.get("totalRevenue", report.get("total_revenue", 0))
    except Exception as e:
        # Log the error line and still create an error line in the log file
        err_line = f"{now} - Report: ERROR fetching data: {e}"
        try:
            os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        except Exception:
            pass
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(err_line + "\n")
        return {"status": "error", "error": str(e)}

    line = f"{now} - Report: {customers} customers, {orders} orders, {revenue} revenue"
    try:
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    except Exception:
        pass
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")

    return {"status": "ok", "customers": customers, "orders": orders, "revenue": revenue}
