from sqlalchemy import Enum as SqlEnum, DateTime, String, ForeignKey, text
from sqlalchemy.orm import mapped_column, Mapped
from enum import Enum
from backend.core.models.base import Base
from datetime import datetime


class DepositORM(Base):
    __tablename__ = 'deposits'
    deposit_id: Mapped[int] = mapped_column(primary_key=True)
    deposit_name: Mapped[str] = mapped_column(String(20))
    shelf_life: Mapped[int] = mapped_column(nullable=False)
    rate: Mapped[float] = mapped_column(nullable=False)

class ClientORM(Base):
    __tablename__ = 'clients'
    client_id: Mapped[int] = mapped_column(primary_key=True)
    client_name: Mapped[str] = mapped_column(String(20))
    client_patronymic: Mapped[str] = mapped_column(String(20))
    client_surname: Mapped[str] = mapped_column(String(20))
    passport_numb: Mapped[str] = mapped_column(String(11))
    city: Mapped[str] = mapped_column(String(20))
    phone_numb: Mapped[str] = mapped_column(String(12))

class AccountORM(Base):
    __tablename__ = 'accounts'
    account_numb: Mapped[int] = mapped_column(primary_key=True)
    opening_date: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    closing_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    amount_invested: Mapped[int]
    deposit_id: Mapped[int] = mapped_column(ForeignKey('deposits.deposit_id', ondelete='RESTRICT'))
    client_id: Mapped[int] = mapped_column(ForeignKey('clients.client_id', ondelete='RESTRICT'))

class UserRole(str, Enum):
    admin = 'admin'
    deposit_manager = 'deposit_manager'
    bank_operator = 'bank_operator'
    analyst = 'analyst'

class UserORM(Base):
    __tablename__ = 'users'
    user_id: Mapped[int] = mapped_column(primary_key=True)
    user_name: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(256))
    role: Mapped[str] = mapped_column(SqlEnum(UserRole, name = "user_role"), nullable=False)
