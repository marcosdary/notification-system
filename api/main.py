from fastapi import FastAPI
import strawberry
from strawberry.fastapi import GraphQLRouter
from fastapi.middleware.cors import CORSMiddleware

from api.graphql.mutation import Mutation
from api.graphql.query import Query

app = FastAPI(title="Notificação de sistema")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET","POST"],
    allow_headers=["*"],
)

schema = strawberry.Schema(query=Query, mutation=Mutation)

graphql_app = GraphQLRouter(schema=schema)

app.include_router(graphql_app, prefix="/graphql")


@app.get("/")
def index():
    return {
        "version": "1.0.0",
        "name": "Notification System"
    }

