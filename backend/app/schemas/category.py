from pydantic import BaseModel, Field, ConfigDict
from typing import Literal


# Data received when creating a category
class CategoryCreate(BaseModel):
    category_name: str = Field(min_length=1, max_length=100)
    category_type: Literal["INCOME", "EXPENSE"]


# Data received when updating a category
class CategoryUpdate(BaseModel):
    category_name: str | None = Field(default=None, max_length=100)
    category_type: Literal["INCOME", "EXPENSE"] | None = None


# Data returned to frontend
class CategoryResponse(BaseModel):
    category_id: int
    user_id: int | None
    category_name: str
    category_type: str

    model_config = ConfigDict(from_attributes=True)