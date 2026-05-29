from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class SplitwiseBalance(Base):
    __tablename__ = "splitwise_balances"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    friend_name: Mapped[str] = mapped_column(String(255), nullable=False)
    friend_id: Mapped[str] = mapped_column(String(100), nullable=False)
    balance: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    updated_at: Mapped[str] = mapped_column(DateTime, server_default=func.now(), nullable=False)


class SplitwiseConnection(Base):
    __tablename__ = "splitwise_connections"
    __table_args__ = (UniqueConstraint("user_id", name="uq_splitwise_connections_user"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    access_token_encrypted: Mapped[str] = mapped_column(Text, nullable=False)
    updated_at: Mapped[str] = mapped_column(DateTime, server_default=func.now(), nullable=False)
