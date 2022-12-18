# from fastapi import FastAPI
# from fastapi_amis_admin.admin.settings import Settings
# from fastapi_amis_admin.admin.site import AdminSite
# # create FastAPI application
# app = FastAPI()
# # create AdminSite instance
# site = AdminSite(settings=Settings(database_url_async='sqlite+aiosqlite:///amisadmin.db'))
# # mount AdminSite instance
# site.mount_app(app)
import core.load_env
from core.app import create_app
from core.project_settings import settings

application = create_app()


@application.on_event("startup")
async def startup_event():
    try:
        pass
        # do anything you want on startup
        # like data seeding or admin creation.
    except:
        pass


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:application", host=settings().HOST_URL, port=settings().HOST_PORT, reload=True)
