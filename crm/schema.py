import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from django.db import IntegrityError, transaction
from .models import Customer, Product, Order
from .filters import CustomerFilter, ProductFilter, OrderFilter
from decimal import Decimal
import re

PHONE_REGEX = re.compile(r'^(\+\d{1,3}\d{4,}|\d{3}-\d{3}-\d{4})$')


# Nodes / Types
class CustomerNode(DjangoObjectType):
    class Meta:
        model = Customer
        interfaces = (relay.Node,)
        fields = '__all__'


class ProductNode(DjangoObjectType):
    class Meta:
        model = Product
        interfaces = (relay.Node,)
        fields = '__all__'


class OrderNode(DjangoObjectType):
    class Meta:
        model = Order
        interfaces = (relay.Node,)
        fields = '__all__'


# Query
class Query(graphene.ObjectType):
    hello = graphene.String()

    all_customers = DjangoFilterConnectionField(
        CustomerNode, filterset_class=CustomerFilter, order_by=graphene.String()
    )
    all_products = DjangoFilterConnectionField(
        ProductNode, filterset_class=ProductFilter, order_by=graphene.String()
    )
    all_orders = DjangoFilterConnectionField(
        OrderNode, filterset_class=OrderFilter, order_by=graphene.String()
    )

    def resolve_hello(self, info):
        return "Hello, GraphQL!"


# Input types
class CustomerInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    email = graphene.String(required=True)
    phone = graphene.String()


class ProductInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    price = graphene.Decimal(required=True)
    stock = graphene.Int()


class OrderInput(graphene.InputObjectType):
    customer_id = graphene.ID(required=True)
    product_id = graphene.ID(required=True)
    quantity = graphene.Int(required=True)


# Mutations
class CreateCustomer(graphene.Mutation):
    class Arguments:
        input = CustomerInput(required=True)

    customer = graphene.Field(CustomerNode)
    message = graphene.String()
    ok = graphene.Boolean()

    @staticmethod
    def validate_phone(phone):
        if phone is None or phone == "":
            return True
        return bool(PHONE_REGEX.match(phone))

    @classmethod
    def mutate(cls, root, info, input):
        name = input.name.strip()
        email = input.email.strip().lower()
        phone = input.phone or None

        if not cls.validate_phone(phone):
            return CreateCustomer(customer=None, message="Invalid phone format", ok=False)

        try:
            customer = Customer.objects.create(name=name, email=email, phone=phone)
            return CreateCustomer(customer=customer, message="Customer created", ok=True)
        except IntegrityError:
            return CreateCustomer(customer=None, message="Email already exists", ok=False)


class CreateProduct(graphene.Mutation):
    class Arguments:
        input = ProductInput(required=True)

    product = graphene.Field(ProductNode)
    message = graphene.String()
    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, input):
        try:
            product = Product.objects.create(
                name=input.name.strip(),
                price=Decimal(input.price),
                stock=input.stock or 0,
            )
            return CreateProduct(product=product, message="Product created", ok=True)
        except Exception as e:
            return CreateProduct(product=None, message=str(e), ok=False)


class CreateOrder(graphene.Mutation):
    class Arguments:
        input = OrderInput(required=True)

    order = graphene.Field(OrderNode)
    message = graphene.String()
    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, input):
        try:
            customer = Customer.objects.get(pk=input.customer_id)
            product = Product.objects.get(pk=input.product_id)

            if input.quantity <= 0:
                return CreateOrder(order=None, message="Quantity must be positive", ok=False)

            if product.stock < input.quantity:
                return CreateOrder(order=None, message="Not enough stock", ok=False)

            with transaction.atomic():
                order = Order.objects.create(
                    customer=customer, product=product, quantity=input.quantity
                )
                product.stock -= input.quantity
                product.save()

            return CreateOrder(order=order, message="Order created", ok=True)
        except Customer.DoesNotExist:
            return CreateOrder(order=None, message="Customer not found", ok=False)
        except Product.DoesNotExist:
            return CreateOrder(order=None, message="Product not found", ok=False)
        except Exception as e:
            return CreateOrder(order=None, message=str(e), ok=False)


# Root Mutation
class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    create_product = CreateProduct.Field()
    create_order = CreateOrder.Field()


# Schema
schema = graphene.Schema(query=Query, mutation=Mutation)
