import strawberry

from app.graphql.mutations import EmailMutation

@strawberry.type
class Mutation(EmailMutation):
    pass