from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import (
    BigInteger,
    String,
    Text,
    Numeric,
    Boolean,
    SmallInteger,
    Date,
    ForeignKey,
    UniqueConstraint,
    CheckConstraint,
    Identity,
    func
)

from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


# ==========================================
# 1. USER MODEL
# ==========================================

class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(always=True),
        primary_key=True
    )

    full_name: Mapped[str] = mapped_column(String(100), nullable=False)

    email: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False
    )

    password_hash: Mapped[str] = mapped_column(Text, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )


# ==========================================
# 2. WALLET MODEL
# ==========================================

class Wallet(Base):
    __tablename__ = "wallets"

    __table_args__ = (
        CheckConstraint(
            "initial_balance >= 0",
            name="chk_wallets_balance"
        ),
        UniqueConstraint(
            "user_id", "wallet_name",
            name="uq_wallets_user_name"
        )
    )

    wallet_id: Mapped[int] = mapped_column(
        BigInteger, Identity(always=True), primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.user_id"), nullable=False
    )

    wallet_name: Mapped[str] = mapped_column(
        String(100), nullable=False
    )

    initial_balance: Mapped[Decimal] = mapped_column(
        Numeric(15, 2), nullable=False, default=Decimal("0")
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True
    )

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )


# ==========================================
# 3. CATEGORY MODEL
# ==========================================

class Category(Base):
    __tablename__ = "categories"

    __table_args__ = (
        CheckConstraint(
            "category_type IN ('INCOME', 'EXPENSE')",
            name="chk_categories_type"
        ),
        UniqueConstraint(
            "user_id", "category_name", "category_type",
            name="uq_categories_user_name_type"
        )
    )

    category_id: Mapped[int] = mapped_column(
        BigInteger, Identity(always=True), primary_key=True
    )

    user_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("users.user_id"), nullable=True
    )

    category_name: Mapped[str] = mapped_column(
        String(100), nullable=False
    )

    category_type: Mapped[str] = mapped_column(
        String(20), nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )


# ==========================================
# 4. TRANSACTION MODEL
# ==========================================

class Transaction(Base):
    __tablename__ = "transactions"

    __table_args__ = (
        CheckConstraint("amount > 0", name="chk_transactions_amount"),
        CheckConstraint(
            "transaction_type IN ('INCOME', 'EXPENSE')",
            name="chk_transactions_type"
        )
    )

    transaction_id: Mapped[int] = mapped_column(
        BigInteger, Identity(always=True), primary_key=True
    )

    wallet_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("wallets.wallet_id"), nullable=False
    )

    category_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("categories.category_id"), nullable=False
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(15, 2), nullable=False
    )

    transaction_type: Mapped[str] = mapped_column(
        String(20), nullable=False
    )

    transaction_date: Mapped[date] = mapped_column(
        Date, nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )


# ==========================================
# 5. BUDGET MODEL
# ==========================================

class Budget(Base):
    __tablename__ = "budgets"

    __table_args__ = (
        CheckConstraint("month BETWEEN 1 AND 12", name="chk_budgets_month"),
        CheckConstraint("year BETWEEN 2000 AND 9999", name="chk_budgets_year"),
        UniqueConstraint(
            "user_id", "month", "year",
            name="uq_budgets_user_month_year"
        )
    )

    budget_id: Mapped[int] = mapped_column(
        BigInteger, Identity(always=True), primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.user_id"), nullable=False
    )

    budget_name: Mapped[str] = mapped_column(
        String(100), nullable=False
    )

    month: Mapped[int] = mapped_column(SmallInteger, nullable=False)

    year: Mapped[int] = mapped_column(SmallInteger, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )


# ==========================================
# 6. BUDGET CATEGORY MODEL
# ==========================================

class BudgetCategory(Base):
    __tablename__ = "budget_categories"

    __table_args__ = (
        CheckConstraint(
            "limit_amount >= 0",
            name="chk_budget_categories_limit"
        ),
        UniqueConstraint(
            "budget_id", "category_id",
            name="uq_budget_categories"
        )
    )

    budget_category_id: Mapped[int] = mapped_column(
        BigInteger, Identity(always=True), primary_key=True
    )

    budget_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("budgets.budget_id"), nullable=False
    )

    category_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("categories.category_id"), nullable=False
    )

    limit_amount: Mapped[Decimal] = mapped_column(
        Numeric(15, 2), nullable=False
    )