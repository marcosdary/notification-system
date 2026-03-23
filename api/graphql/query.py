import strawberry

from api.graphql.queries.email_notification_query import EmailNotificationQuery

@strawberry.type
class Query(EmailNotificationQuery):
    pass
