from fastapi import APIRouter, HTTPException
from app.database.database import SessionLocal
from app.models.users import User
import logging

logger = logging.getLogger("users-service")
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [USERS SERVICE] - %(message)s')

#prefix agrupa rutas, tags sirven para la UI de docs.
router = APIRouter(prefix="/users", tags=["/users"])

# todos los usuarios
@router.get("/")
def get_users():
    logger.info("GET /users recibido")
    db = SessionLocal()
    users = db.query(User).all()
    db.close()
    
    logger.info(f"BD: Recuperados {len(users)} usuarios")
    return users
    
    
# usuario por ID
@router.get("/{user_id}")
def get_user_by_id(user_id: int):
    logger.info(f"GET /users/{user_id} recibido")
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    db.close()
    
    if not user:
        logger.error(f"Usuario {user_id} no encontrado")
        raise HTTPException(status_code=404, detail="User not found")
    
    logger.info(f"BD: Usuario {user_id} encontrado")
    return user  # Devuelve el objeto User (SQLAlchemy lo serializa a JSON)


# crear usuario
@router.post("/")
def create_user(user: dict):
    logger.info(f"POST /users - Nombre: {user.get('name')}")
    db = SessionLocal()
    new_user = User(name=user["name"]) 
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()
    
    logger.info(f"BD: Usuario creado con ID {new_user.id}")
    return new_user


# eliminar usuario por ID
@router.delete("/{user_id}")
def delete_user(user_id: int):
    logger.info(f"DELETE /users/{user_id} recibido")
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        db.close()
        logger.error(f"Usuario {user_id} no encontrado")
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    db.close()
    
    logger.info(f"BD: Usuario {user_id} eliminado")
    return {"message": f"User with id {user_id} deleted"}
