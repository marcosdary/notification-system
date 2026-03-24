import strawberry

from api.graphql.mutations import EmailNotificationMutation

@strawberry.type
class Mutation(EmailNotificationMutation):
    pass