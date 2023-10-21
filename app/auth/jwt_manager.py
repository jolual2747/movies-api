from typing import Optional
from fastapi import HTTPException
from jwt import encode, decode
from fastapi.security import HTTPBearer
from fastapi import Request

def create_token(data:dict):
    token = encode(payload=data, key = 'secret_key_jeje', algorithm='HS256')
    return token

def validate_token(token:str) -> dict:
    data = decode(token, key='secret_key_jeje', algorithms=['HS256'])
    return data

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data["email"] != "admin@gmail.com":
            raise HTTPException(status_code=403, detail="Invalid credentials!")