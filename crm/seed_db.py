import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'graphql_crm.settings')
django.setup()

from crm.models import Customer, Product

Customer.objects.all().delete()
Product.objects.all().delete()

Customer.objects.create(name='Alice', email='alice@example.com', phone='+123456789')
Customer.objects.create(name='Bob', email='bob@example.com', phone='+198765432')

Product.objects.create(name='Laptop', price=1200.50, stock=5)
Product.objects.create(name='Phone', price=650.00, stock=10)

print("Database seeded successfully!")