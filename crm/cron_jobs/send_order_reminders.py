#!/usr/bin/env python3
"""
Query the GraphQL endpoint for orders created in the last 7 days
and log reminders to /tmp/order_reminders_log.txt
"""

from datetime import datetime, timedelta, timezone
from pathlib import Path
import sys

# If you prefer using the gql package, it's fine—but to minimize deps here,
# we'll use requests. (You listed gql in the brief; we'll still include it in requirements)
import requests

GRAPHQL_URL = "http://localhost:8000/graphql"
LOG_FILE = Path("/tmp/order_reminders_log.txt")

QUERY = """
query RecentOrders($first:Int) {
  allOrders(first:$first) {
    edges {
      node {
        id
        orderDate
        customer { email }
      }
    }
  }
}
"""

def main():
    try:
        resp = requests.post(GRAPHQL_URL, json={"query": QUERY, "variables": {"first": 1000}})
        resp.raise_for_status()
        data = resp.json()
        edges = data.get("data", {}).get("allOrders", {}).get("edges", [])
    except Exception as e:
        print(f"Failed to query GraphQL: {e}", file=sys.stderr)
        return

    now = datetime.now(timezone.utc)
    week_ago = now - timedelta(days=7)

    lines = []
    for edge in edges:
        node = edge.get("node", {})
        od = node.get("orderDate")
        email = (node.get("customer") or {}).get("email")
        if not od or not email:
            continue
        try:
            # Graphene returns ISO 8601 strings
            od_dt = datetime.fromisoformat(od.replace("Z", "+00:00"))
        except Exception:
            continue

        if od_dt >= week_ago:
            lines.append(f"{now:%Y-%m-%d %H:%M:%S} - Order {node.get('id')} -> {email}")

    if lines:
        with LOG_FILE.open("a", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")

    print("Order reminders processed!")

if __name__ == "__main__":
    main()
