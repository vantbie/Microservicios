from sqlalchemy import Column, Integer, String, Float
from ..database.database import Base
from pydantic import BaseModel
from typing import Optional

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)

class ProductCreate(BaseModel):
    name: str
    price: float
    
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None