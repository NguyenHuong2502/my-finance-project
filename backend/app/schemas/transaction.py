from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field, ConfigDict
from typing import Literal


# Data received when creating a transaction
class TransactionCreate(BaseModel):
    wallet_id: int
    category_id: int
    amount: Decimal = Field(gt=0)
    transaction_type: Literal["INCOME", "EXPENSE"]
    transaction_date: date
    description: str | None = None


# Data received when updating a transaction
class TransactionUpdate(BaseModel):
    wallet_id: int | None = None
    category_id: int | None = None
    amount: Decimal | None = Field(default=None, gt=0)
    transaction_type: Literal["INCOME", "EXPENSE"] | None = None
    transaction_date: date | None = None
    description: str | None = None


# Data returned to frontend
class TransactionResponse(BaseModel):
    transaction_id: int
    wallet_id: int
    category_id: int
    amount: Decimal
    transaction_type: str
    transaction_date: date
    description: str | None

    model_config = ConfigDict(from_attributes=True)