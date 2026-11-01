from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict


# Data received when creating a wallet
class WalletCreate(BaseModel):
    wallet_name: str = Field(min_length=1, max_length=100)
    initial_balance: Decimal = Field(default=Decimal("0"), ge=0)


# Data received when updating a wallet
class WalletUpdate(BaseModel):
    wallet_name: str | None = Field(default=None, max_length=100)
    initial_balance: Decimal | None = Field(default=None, ge=0)
    is_active: bool | None = None


# Data returned to frontend
class WalletResponse(BaseModel):
    wallet_id: int
    user_id: int
    wallet_name: str
    initial_balance: Decimal
    is_active: bool

    model_config = ConfigDict(from_attributes=True)