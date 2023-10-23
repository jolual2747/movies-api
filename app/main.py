from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from config.database import engine, base
from app.middlewares.error_handler import ErrorHandler
from app.routers.movie import movie_router
from app.routers.user import login_router

app = FastAPI()
app.title = "App para Movies"
app.version = "0.0.1"

app.add_middleware(ErrorHandler)

base.metadata.create_all(bind = engine)

routers = [movie_router, login_router]
for router in routers:
    app.include_router(router)

@app.get("/", tags=["home"])
def message():
    return HTMLResponse("<h1>Hello world</h1>")