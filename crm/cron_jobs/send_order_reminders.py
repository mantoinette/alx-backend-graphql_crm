#!/usr/bin/env python3
import sys
import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# Configure GraphQL endpoint
transport = RequestsHTTPTransport(
    url="http://localhost:8000/graphql",
    verify=True,
    retries=3,
)

client = Client(transport=transport, fetch_schema_from_transport=True)

# Calculate cutoff (last 7 days)
cutoff = (datetime.datetime.now() - datetime.timedelta(days=7)).date().isoformat()

# GraphQL query
query = gql(
    """
    query getRecentOrders($cutoff: Date!) {
      orders(orderDate_Gte: $cutoff) {
        id
        customer {
          email
        }
      }
    }
    """
)

# Execute query
try:
    result = client.execute(query, variable_values={"cutoff": cutoff})
    orders = result.get("orders", [])
except Exception as e:
    sys.stderr.write(f"GraphQL query failed: {e}\n")
    sys.exit(1)

# Log orders
log_path = "/tmp/order_reminders_log.txt"
with open(log_path, "a") as f:
    for order in orders:
        order_id = order.get("id")
        email = order.get("customer", {}).get("email")
        f.write(f"{datetime.datetime.now()} - Order {order_id}, Email: {email}\n")

print("Order reminders processed!")
