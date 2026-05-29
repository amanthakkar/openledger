from datetime import date

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, Numeric, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class PlaidItem(Base):
    __tablename__ = "plaid_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    institution_name: Mapped[str] = mapped_column(String(255), nullable=False)
    institution_id: Mapped[str] = mapped_column(String(100), nullable=False)
    access_token_encrypted: Mapped[str] = mapped_column(Text, nullable=False)
    cursor: Mapped[str | None] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(50), default="healthy", nullable=False)
    last_synced_at: Mapped[str | None] = mapped_column(DateTime)
    created_at: Mapped[str] = mapped_column(DateTime, server_default=func.now(), nullable=False)


class Account(Base):
    __tablename__ = "accounts"
    __table_args__ = (UniqueConstraint("plaid_account_id", name="uq_accounts_plaid_account_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    plaid_item_id: Mapped[int] = mapped_column(ForeignKey("plaid_items.id"), nullable=False)
    plaid_account_id: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    official_name: Mapped[str | None] = mapped_column(String(255))
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    subtype: Mapped[str | None] = mapped_column(String(50))
    current_balance: Mapped[float | None] = mapped_column(Numeric(12, 2))
    available_balance: Mapped[float | None] = mapped_column(Numeric(12, 2))
    currency: Mapped[str] = mapped_column(String(3), default="USD", nullable=False)
    is_hidden: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    updated_at: Mapped[str | None] = mapped_column(DateTime)


class Transaction(Base):
    __tablename__ = "transactions"
    __table_args__ = (UniqueConstraint("plaid_transaction_id", name="uq_transactions_plaid_transaction_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"), nullable=False)
    plaid_transaction_id: Mapped[str] = mapped_column(String(255), nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    merchant_name: Mapped[str | None] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(String(500))
    amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    category: Mapped[str | None] = mapped_column(String(100))
    subcategory: Mapped[str | None] = mapped_column(String(100))
    is_recurring: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_excluded: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[str] = mapped_column(DateTime, server_default=func.now(), nullable=False)
