import strawberry
# from strawberry.fastapi import GraphQLRouter
# from strawberry.schema.config import StrawberryConfig
# from src.graphql.schemas.query_schema import Query

from src.routes import access_routs,google_login_routs

# schema = strawberry.Schema(query=Query,config=StrawberryConfig(auto_camel_case=True))
# graphql_app = GraphQLRouter(schema)
api_url : str = "/api"

def registering_routes(app):
    app.include_router(access_routs.router, prefix=api_url)
    app.include_router(google_login_routs.router, prefix=api_url)
    # app.include_router(auth_routes.router, prefix=api_url)
    # app.include_router(graphql_app, prefix="/graphql")