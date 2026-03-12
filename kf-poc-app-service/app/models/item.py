from pydantic import BaseModel, Field
from typing import Optional

class Item(BaseModel):
    id: Optional[int] = Field(default=None, ge=0)
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: float = Field(..., gt=0, le=1000000)
    category: Optional[str] = Field(default="general", max_length=50)
    in_stock: bool = Field(default=True)
