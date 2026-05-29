from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Holding(Base):
    __tablename__ = "holdings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"), nullable=False)
    security_name: Mapped[str] = mapped_column(String(255), nullable=False)
    ticker: Mapped[str | None] = mapped_column(String(20))
    quantity: Mapped[float] = mapped_column(Numeric(14, 6), nullable=False)
    price: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    value: Mapped[float] = mapped_column(Numeric(14, 2), nullable=False)
    cost_basis: Mapped[float | None] = mapped_column(Numeric(14, 2))
    updated_at: Mapped[str] = mapped_column(DateTime, server_default=func.now(), nullable=False)
