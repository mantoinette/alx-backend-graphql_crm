from gql.transport.requests import RequestsHTTPTransport
from gql import gql, Client
from datetime import datetime
from pathlib import Path
import requests

HEARTBEAT_LOG = Path("/tmp/crm_heartbeat_log.txt")
LOW_STOCK_LOG = Path("/tmp/low_stock_updates_log.txt")
GRAPHQL_URL = "http://localhost:8000/graphql"

def log_crm_heartbeat():
    """
    Logs 'DD/MM/YYYY-HH:MM:SS CRM is alive' every 5 minutes.
    Optionally hits the GraphQL hello field; failure is ignored.
    """
    ts = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    line = f"{ts} CRM is alive"
    try:
        HEARTBEAT_LOG.parent.mkdir(parents=True, exist_ok=True)
        with HEARTBEAT_LOG.open("a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass

    # Optional GraphQL ping (non-fatal)
    try:
        q = {"query": "query { hello }"}
        requests.post(GRAPHQL_URL, json=q, timeout=5)
    except Exception:
        pass


def update_low_stock():
    """
    Calls a GraphQL mutation to restock products with stock < 10 by +10.
    Logs updated product names and new stock to /tmp/low_stock_updates_log.txt
    """
    mutation = """
    mutation {
      updateLowStockProducts {
        ok
        message
        updatedProducts {
          id
          name
          stock
        }
      }
    }
    """
    try:
        resp = requests.post(GRAPHQL_URL, json={"query": mutation}, timeout=30)
        resp.raise_for_status()
        data = resp.json().get("data", {}).get("updateLowStockProducts", {})
        products = data.get("updatedProducts") or []
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        lines = [f"{ts} - Restocked {len(products)} products"]
        for p in products:
            lines.append(f"- {p['name']}: stock={p['stock']}")
        LOW_STOCK_LOG.parent.mkdir(parents=True, exist_ok=True)
        with LOW_STOCK_LOG.open("a", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
    except Exception as e:
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with LOW_STOCK_LOG.open("a", encoding="utf-8") as f:
            f.write(f"{ts} - ERROR: {e}\n")
