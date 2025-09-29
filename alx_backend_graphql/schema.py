# alx-backend-graphql_crm/schema.py
# REPLACE your current schema.py with this

import graphene
from crm.schema import Query as CRMQuery


class Query(CRMQuery, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)