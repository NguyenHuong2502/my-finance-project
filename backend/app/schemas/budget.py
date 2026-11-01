from decimal import Decimal

from pydantic import BaseModel, Field, ConfigDict


# Data received when creating a budget
class BudgetCreate(BaseModel):
    budget_name: str = Field(min_length=1, max_length=100)
    month: int = Field(ge=1, le=12)
    year: int = Field(ge=2000, le=9999)


# Data received when adding a category to a budget
class BudgetCategoryCreate(BaseModel):
    category_id: int
    limit_amount: Decimal = Field(ge=0)


# Data returned to frontend
class BudgetResponse(BaseModel):
    budget_id: int
    user_id: int
    budget_name: str
    month: int
    year: int

    model_config = ConfigDict(from_attributes=True)


class BudgetCategoryResponse(BaseModel):
    budget_category_id: int
    budget_id: int
    category_id: int
    limit_amount: Decimal

    model_config = ConfigDict(from_attributes=True)