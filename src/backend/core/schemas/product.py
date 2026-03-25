from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field

from backend.core.schemas.category import CategoryResponse


class ProductBase(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Product name",
    )

    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(
        ...,
        gt=0,
        description="Product price (must be greater than 0)",
    )
    category_id: int = Field(..., description="Category id")
    image_url: Optional[str] = Field(None, description="Image url")


class ProductCreate(ProductBase):
    pass


class ProductResponse(BaseModel):
    id: int = Field(..., description="Product ID")
    name: str
    description: Optional[str]
    price: float
    category_id: int
    image_url: Optional[str]
    created_at: datetime
    category: CategoryResponse = Field(..., description="Product category")


class ProductListResponse(BaseModel):
    items: List[ProductResponse]
    total: int = Field(..., description="Total product count")
