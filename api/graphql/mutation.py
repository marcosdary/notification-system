import strawberry

from api.graphql.mutations.email_notification_mutation import EmailNotificationMutation

@strawberry.type
class Mutation(EmailNotificationMutation):
    pass