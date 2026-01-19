from fastapi import APIRouter
from app.auth.jwt_utils import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
def login():
#Login simple para pruebas, luego puede conectarse a Users.

    access_token = create_access_token(data={"sub": "test_user"})

    return {"access_token": access_token, "token_type": "bearer"}
