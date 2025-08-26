from datetime import datetime
from pathlib import Path

LOG_PATH = "/tmp/crm_heartbeat_log.txt"

def log_crm_heartbeat():
    """
    Logs a line like:
    DD/MM/YYYY-HH:MM:SS CRM is alive
    to /tmp/crm_heartbeat_log.txt (append mode).
    Optionally pings the GraphQL hello field if 'requests' is available.
    """
    ts = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    line = f"{ts} CRM is alive"

    # Ensure parent dir exists (best-effort; /tmp usually exists)
    try:
        Path(LOG_PATH).parent.mkdir(parents=True, exist_ok=True)
    except Exception:
        pass

    # Append heartbeat
    try:
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        # Don't crash the cron job if logging fails
        return

    # --- Optional: GraphQL hello check ---
    try:
        import requests  # optional dependency
        resp = requests.post(
            "http://localhost:8000/graphql",
            json={"query": "query { hello }"},
            timeout=3,
        )
        extra = ""
        if resp.ok:
            data = resp.json() if resp.headers.get("content-type", "").lower().startswith("application/json") else {}
            hello_val = (data or {}).get("data", {}).get("hello")
            extra = f" GraphQL hello: {hello_val}"
        else:
            extra = f" GraphQL check failed HTTP {resp.status_code}"

        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(f"{ts}{extra}\n")
    except Exception:
        # Silently ignore optional GraphQL issues/missing requests
        pass
