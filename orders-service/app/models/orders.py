from sqlalchemy import Column, Integer
from ..database.database import Base

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer)
    quantity = Column(Integer)