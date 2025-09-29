# alx_backend_graphql_crm/schema.py

import graphene


class Query(graphene.ObjectType):
    """
    Root Query class for GraphQL schema
    """
    hello = graphene.String(default_value="Hello, GraphQL!")
    
    def resolve_hello(self, info):
        """
        Resolver for the hello field
        Returns a greeting message
        """
        return "Hello, GraphQL!"


# Create the schema
schema = graphene.Schema(query=Query)