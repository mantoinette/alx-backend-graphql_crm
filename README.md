# alx-backend-graphql_crm

A **Django + Graphene GraphQL CRM** example project for the ALX backend curriculum modules:

- **Understanding GraphQL**
- **Crons: Scheduling and Automating Tasks**

This project implements a **Customer Relationship Management (CRM)** system with models for **Customer, Product, and Order**, a **GraphQL API**, and **automation scripts** for cleaning inactive customers, sending order reminders, logging heartbeats, and updating stock.

---

## 🚀 Features

- GraphQL API with queries, filters, and mutations
- Models: `Customer`, `Product`, `Order`
- Scripts for:

  - Cleaning inactive customers
  - Sending order reminders
  - Logging heartbeat with `django-crontab`
  - Updating low-stock products via GraphQL mutation

- Optional: Weekly report generation with Celery

---

## ⚡ Quick Start

1. **Create virtual environment**

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Linux / Mac
   .venv\Scripts\activate      # Windows
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations**

   ```bash
   python manage.py migrate
   ```

4. **Create superuser (optional)**

   ```bash
   python manage.py createsuperuser
   ```

5. **Seed sample data**

   ```bash
   python manage.py shell < crm/seed_db.py
   ```

6. **Run server**

   ```bash
   python manage.py runserver
   ```

7. **Access GraphQL Playground**

   - GraphiQL UI: [http://localhost:8000/graphql](http://localhost:8000/graphql)

---

## 📚 GraphQL API

### Queries

- `customers` — list and filter customers
- `products` — list and filter products
- `orders` — list and filter orders

### Mutations

- `createCustomer`, `createProduct`, `createOrder`
- `updateLowStockProducts` (automated mutation for stock replenishment)

---

## 🛠️ Automation & Cron Jobs

### 0. Customer Cleanup

- **Script**: `crm/cron_jobs/clean_inactive_customers.sh`
- **Runs**: Every Sunday at 2:00 AM
- **Logs**: `/tmp/customer_cleanup_log.txt`

### 1. Order Reminder

- **Script**: `crm/cron_jobs/send_order_reminders.py`
- **Runs**: Daily at 8:00 AM
- **Logs**: `/tmp/order_reminders_log.txt`

### 2. Heartbeat Logger

- **App**: `django-crontab`
- **Runs**: Every 5 minutes
- **Logs**: `/tmp/crm_heartbeat_log.txt`

Manage crontab:

```bash
python manage.py crontab add      # add jobs
python manage.py crontab show     # list jobs
python manage.py crontab remove   # clear jobs
```

### 3. Stock Alert & Auto-Update

- **Mutation**: `updateLowStockProducts`
- **Cron**: Every 12 hours
- **Logs**: `/tmp/low_stock_updates_log.txt`

---

## 📊 Optional: Celery Weekly Reports

- **Setup Celery & Beat**

  - File: `crm/celery.py` (Celery app)
  - File: `crm/tasks.py` (scheduled tasks)

- **Task**: `generate_crm_report`

  - Runs every Monday at 6:00 AM
  - Fetches total customers, orders, and revenue
  - Logs results to `/tmp/crm_report_log.txt`

- **Run Celery**

  ```bash
  celery -A crm worker -l info
  celery -A crm beat -l info
  ```

---

## 📂 Project Structure

```
alx_backend_graphql_crm/
│── crm/
│   ├── models.py
│   ├── schema.py
│   ├── cron.py
│   ├── tasks.py (optional Celery)
│   ├── cron_jobs/
│   │   ├── clean_inactive_customers.sh
│   │   ├── customer_cleanup_crontab.txt
│   │   ├── send_order_reminders.py
│   │   ├── order_reminders_crontab.txt
│   └── seed_db.py
│
├── manage.py
├── requirements.txt
└── README.md
```

---

## 🧪 Testing Cron Jobs

Run scripts manually before scheduling:

```bash
bash crm/cron_jobs/clean_inactive_customers.sh
python crm/cron_jobs/send_order_reminders.py
python manage.py runscript crm.cron.log_crm_heartbeat
```
