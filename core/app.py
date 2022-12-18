from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from core.routes import registering_routes
from helpers.middleware import registering_middleware


def create_app():
    app = FastAPI()
    app.mount("/static", StaticFiles(directory="build/static"), name="static")
    registering_middleware(app)
    registering_routes(app)
    return app
