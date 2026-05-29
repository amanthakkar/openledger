from datetime import date

from sqlalchemy import Date, ForeignKey, Integer, Numeric, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class NetWorthSnapshot(Base):
    __tablename__ = "net_worth_snapshots"
    __table_args__ = (UniqueConstraint("user_id", "date", name="uq_net_worth_snapshots_user_date"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    total_assets: Mapped[float] = mapped_column(Numeric(14, 2), nullable=False)
    total_liabilities: Mapped[float] = mapped_column(Numeric(14, 2), nullable=False)
    net_worth: Mapped[float] = mapped_column(Numeric(14, 2), nullable=False)
    breakdown: Mapped[dict] = mapped_column(JSONB, nullable=False)
