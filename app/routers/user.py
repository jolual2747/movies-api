from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.middlewares.jwt_bearer import create_token
from app.schemas.user import User

login_router = APIRouter()

@login_router.post('/login', tags = ["auth"])
def login(user:User):
    if user.email == 'admin@gmail.com' and user.password == "admin":
        token = create_token(user.model_dump())
        return JSONResponse(status_code=200, content=token)