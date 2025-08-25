from celery import shared_task
from datetime import datetime
from pathlib import Path
import requests

GRAPHQL_URL = "http://localhost:8000/graphql"
REPORT_LOG = Path("/tmp/crm_report_log.txt")

QUERY = """
query ReportData($first:Int){
  allCustomers { pageInfo { hasNextPage } }  # we just need existence to count via a dedicated field if available
  allOrders(first:$first){
    edges {
      node {
        id
        totalAmount
      }
    }
  }
}
"""

# Optional: if your schema has dedicated aggregate fields, replace the query above with them.
COUNT_CUSTOMERS = """
query { allCustomers { edges { node { id } } } }
"""

@shared_task
def generate_crm_report():
    """
    Uses GraphQL to compute simple totals and logs them.
    NOTE: This example pulls orders (first 1000) and sums totalAmount client-side.
    For large datasets, add proper aggregate fields in your schema.
    """
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        # Count customers (basic approach)
        r1 = requests.post(GRAPHQL_URL, json={"query": COUNT_CUSTOMERS}, timeout=60)
        r1.raise_for_status()
        cust_edges = r1.json().get("data", {}).get("allCustomers", {}).get("edges", [])
        total_customers = len(cust_edges)

        # Orders and revenue (limited)
        r2 = requests.post(GRAPHQL_URL, json={"query": QUERY, "variables": {"first": 1000}}, timeout=60)
        r2.raise_for_status()
        orders = (r2.json().get("data", {}).get("allOrders", {}) or {}).get("edges", [])
        total_orders = len(orders)
        total_revenue = 0.0
        for e in orders:
            node = e.get("node") or {}
            amt = node.get("totalAmount")
            if amt is None:
                continue
            try:
                total_revenue += float(amt)
            except Exception:
                pass

        REPORT_LOG.parent.mkdir(parents=True, exist_ok=True)
        with REPORT_LOG.open("a", encoding="utf-8") as f:
            f.write(f"{ts} - Report: {total_customers} customers, {total_orders} orders, {total_revenue:.2f} revenue\n")
    except Exception as e:
        with REPORT_LOG.open("a", encoding="utf-8") as f:
            f.write(f"{ts} - ERROR generating report: {e}\n")
