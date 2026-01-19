from fastapi import APIRouter, Depends
from app.auth.auth import verify_token
from app.models.users import UserCreate
import requests
import json
import logging

logger = logging.getLogger("api-gateway")
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [API GATEWAY] - %(message)s')

router = APIRouter(prefix="/users", tags=["users"])

USERS_SERVICE_URL = "http://localhost:8001/users"

# GET: todos los usuarios
@router.get("/")
def proxy_list_users(token: str = Depends(verify_token)):
    
    logger.info("GET /users recibido")
    
    headers = {"Authorization": f"Bearer {token}"}
    logger.info(f"Llamando Users Service: {USERS_SERVICE_URL}")
    
    response = requests.get(USERS_SERVICE_URL, headers=headers)
    try:
        data = response.json()
        logger.info(f"Respuesta exitosa - {len(data)} usuarios recuperados")
    except:
        logger.error(f"Error en respuesta: {response.text}")
    return response.json()

# GET por ID
@router.get("/{user_id}")
def proxy_user_id(user_id: int, token: str = Depends(verify_token)):
    
    logger.info(f"GET /users/{user_id} recibido")
    
    headers = {"Authorization": f"Bearer {token}"}
    logger.info(f"Llamando Users Service: {USERS_SERVICE_URL}/{user_id}")
    
    response = requests.get(f"{USERS_SERVICE_URL}/{user_id}", headers=headers)
    try:
        data = response.json()
        logger.info(f"Usuario {user_id} recuperado exitosamente")
    except:
        logger.error(f"Error en respuesta: {response.text}")
    return response.json()

# POST: crear usuario
@router.post("/")
def proxy_create_user(user: UserCreate, token: str = Depends(verify_token)):
    
    logger.info(f"POST /users - Nombre: {user.name}")
    
    headers = {"Authorization": f"Bearer {token}"}
    logger.info(f"Llamando Users Service: {USERS_SERVICE_URL}")
    
    response = requests.post(USERS_SERVICE_URL, json=user.dict(), headers=headers)
    try:
        data = response.json()
        logger.info("Usuario creado exitosamente")
    except:
        logger.error(f"Error en respuesta: {response.text}")
    return response.json()

# DELETE por ID
@router.delete("/{user_id}")
def proxy_delete_user(user_id: int, token: str = Depends(verify_token)):
    
    logger.info(f"DELETE /users/{user_id} recibido")
    
    headers = {"Authorization": f"Bearer {token}"}
    logger.info(f"Llamando Users Service: {USERS_SERVICE_URL}/{user_id}")
    
    response = requests.delete(f"{USERS_SERVICE_URL}/{user_id}", headers=headers)
    try:
        data = response.json()
        logger.info(f"Usuario {user_id} eliminado exitosamente")
    except:
        logger.error(f"Error en respuesta: {response.text}")
    return response.json()


    


