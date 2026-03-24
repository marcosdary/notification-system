import strawberry

from api.graphql.queries import EmailNotificationQuery

@strawberry.type
class Query(EmailNotificationQuery):
    pass
