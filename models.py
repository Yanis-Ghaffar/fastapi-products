from sqlalchemy import Column, Integer, String, Float
from database import Base
from pydantic import BaseModel

# Modèle SQLAlchemy (table en base)
class ProductModel(Base):
    __tablename__ = "products"

    id       = Column(Integer, primary_key=True, index=True)
    name     = Column(String)
    description = Column(String)
    price    = Column(Float)
    quantity = Column(Integer)

# Modèle Pydantic (validation des requêtes)
class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float
    quantity: int

    class Config:
        from_attributes = True  # permet la conversion ORM → Pydantic