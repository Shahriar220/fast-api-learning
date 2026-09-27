from typing import Optional
from pydantic import BaseModel, ConfigDict

# Shared properties
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    quantity: int

# Properties to receive on product creation (no ID)
class ProductCreate(ProductBase):
    pass

# Properties to receive on product update (all fields optional)
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None

# Properties to return to client (includes DB ID)
class ProductResponse(ProductBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
