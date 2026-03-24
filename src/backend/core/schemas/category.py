from pydantic import BaseModel, Field, ConfigDict


class CategoryBase(BaseModel):
    name: str = Field(
        ...,
        min_length=5,
        max_length=100,
        description="Category name",
    )
    slug: str = Field(
        ...,
        min_length=5,
        max_length=100,
        description="Category slug",
    )


class CategoryCreate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Unique category ID")
