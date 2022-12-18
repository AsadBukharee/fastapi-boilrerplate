from fastapi.middleware.cors import CORSMiddleware
from src.constants.origins_enum import origins


def registering_middleware(application):
    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "HEAD", "OPTIONS", "PUT", "DELETE"],
        allow_headers=["Access-Control-Allow-Headers","Set-Cookie", 'Content-Type', 'Authorization', 'Access-Control-Allow-Origin'],
    )