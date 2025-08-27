# crm/schema.py
import graphene
from graphene_django import DjangoObjectType
from crm.models import Product  # adjust if your model is elsewhere

class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ("id", "name", "stock")

class UpdateLowStockProducts(graphene.Mutation):
    ok = graphene.Boolean()
    message = graphene.String()
    updated_products = graphene.List(ProductType)

    class Arguments:
        # no args; it just finds low-stock items and restocks them
        pass

    @classmethod
    def mutate(cls, root, info):
        low = Product.objects.filter(stock__lt=10)
        updated = []
        for p in low:
            p.stock = (p.stock or 0) + 10
            p.save(update_fields=["stock"])
            updated.append(p)

        msg = f"Restocked {len(updated)} products by +10."
        return UpdateLowStockProducts(ok=True, message=msg, updated_products=updated)

# ---- Hook the mutation into your schema ----
# If you already have a Mutation class, just add the field below to it:
#   update_low_stock_products = UpdateLowStockProducts.Field()
class Mutation(graphene.ObjectType):
    update_low_stock_products = UpdateLowStockProducts.Field()

# Keep your existing Query class if you have one.
# This minimal Query is safe if you don't:
class Query(graphene.ObjectType):
    hello = graphene.String(default_value="Hello from CRM")

schema = graphene.Schema(query=Query, mutation=Mutation)
