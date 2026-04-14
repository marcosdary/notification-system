import strawberry

from app.graphql.mutations import EmailNotificationMutation

@strawberry.type
class Mutation(EmailNotificationMutation):
    pass