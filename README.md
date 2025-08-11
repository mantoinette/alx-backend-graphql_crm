# alx-backend-graphql_crm

Django + Graphene GraphQL CRM example for ALX module "Understanding GraphQL". Contains models for Customer, Product, Order and GraphQL schema with queries, filters, and mutations.

## Quick start

1. Create virtual env: `python -m venv .venv` and activate it.
2. Install requirements: `pip install -r requirements.txt`.
3. Run migrations: `python manage.py migrate`.
4. Create superuser (optional): `python manage.py createsuperuser`.
5. Seed sample data: `python manage.py shell < crm/seed_db.py`.
6. Run server: `python manage.py runserver`.
7. Open GraphiQL: `http://localhost:8000/graphql`.
