import strawberry

from app.graphql.queries import EmailNotificationQuery

@strawberry.type
class Query(EmailNotificationQuery):
    pass
