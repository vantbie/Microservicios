from pydantic import BaseModel

#Modelo pydantic para recibir datos del usuario
class UserCreate(BaseModel):
    name: str