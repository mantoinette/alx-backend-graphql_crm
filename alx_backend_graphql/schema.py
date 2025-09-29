# Put this in: alx-backend-graphql_crm/schema.py (or alx_backend_graphql_crm/schema.py)

import graphene


class Query(graphene.ObjectType):
    hello = graphene.String(default_value="Hello, GraphQL!")
    
    def resolve_hello(self, info):
        return "Hello, GraphQL!"


schema = graphene.Schema(query=Query)