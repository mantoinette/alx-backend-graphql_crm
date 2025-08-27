# crm/cron.py
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from datetime import datetime
import os

# Change this if your GraphQL URL differs
GRAPHQL_URL = os.environ.get("GRAPHQL_URL", "http://localhost:8000/graphql/")

LOG_DIR = "/tmp"  # On Windows, this becomes C:\tmp
LOG_FILE = os.path.join(LOG_DIR, "low_stock_updates_log.txt")

def _append_log(line: str) -> None:
    try:
        os.makedirs(LOG_DIR, exist_ok=True)
    except Exception:
        pass
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def update_low_stock():
    """
    Calls the UpdateLowStockProducts GraphQL mutation and logs results with timestamps.
    """
    transport = RequestsHTTPTransport(
        url=GRAPHQL_URL,
        verify=True,
        retries=3,
    )
    client = Client(transport=transport, fetch_schema_from_transport=True)

    # Optional: ping the hello field to confirm endpoint is responsive
    try:
        ping = client.execute(gql("query { hello }"))
        _append_log(f"{datetime.now().isoformat(timespec='seconds')} — hello ping: {ping.get('hello')}")
    except Exception as e:
        _append_log(f"{datetime.now().isoformat(timespec='seconds')} — hello ping failed: {e}")

    mutation = gql("""
        mutation UpdateLowStock {
          updateLowStockProducts {
            ok
            message
            updatedProducts { id name stock }
          }
        }
    """)

    ts = datetime.now().isoformat(timespec="seconds")
    try:
        result = client.execute(mutation)
        payload = result.get("updateLowStockProducts") or {}
        ok = payload.get("ok")
        msg = payload.get("message", "")
        items = payload.get("updatedProducts") or []

        _append_log(f"{ts} — ok={ok} message='{msg}'")
        for p in items:
            _append_log(f"{ts} — {p['name']}: stock={p['stock']}")
    except Exception as e:
        _append_log(f"{ts} — mutation failed: {e}")
