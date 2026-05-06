import strawberry

from app.graphql.queries import EmailQuery

@strawberry.type
class Query(EmailQuery):
    pass
