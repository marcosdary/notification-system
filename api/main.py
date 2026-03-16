from fastapi import FastAPI
import strawberry
from strawberry.fastapi import GraphQLRouter
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Notificação de sistema")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET","POST"],
    allow_headers=["Authorization","Content-Type"],
)

@app.get("/")
def index():
    return {
        "version": "1.0.0",
        "name": "Notification System"
    }

