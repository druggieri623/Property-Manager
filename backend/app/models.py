from enum import Enum
from typing import Optional

from sqlmodel import Field, SQLModel


class DuesPaymentMethod(str, Enum):
    CHECK = "check"
    ACH = "ach"
    ONLINE = "online"


class Owner(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    unit_number: str = Field(index=True, unique=True)
    full_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    mailing_address: Optional[str] = None
    dues_payment_method: DuesPaymentMethod = DuesPaymentMethod.CHECK
    active: bool = True


class ServiceProvider(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    company_name: str = Field(index=True, unique=True)
    contact_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    service_category: Optional[str] = None
    notes: Optional[str] = None
    active: bool = True


class HOASetting(SQLModel, table=True):
    id: Optional[int] = Field(default=1, primary_key=True)
    bank_name: str = "Bluestone Bank"
