from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from app.auth.jwt_utils import verify_jwt_token

api_key_header = APIKeyHeader(name="Authorization",auto_error=False)

def verify_token(token: str = Security(api_key_header)):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token faltante")

    if not token.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Formato de token inválido")

    jwt_token = token.replace("Bearer ", "")
    payload = verify_jwt_token(jwt_token)

    return payload  # info del usuario
