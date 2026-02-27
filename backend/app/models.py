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
    owner_one_full_name: str
    owner_one_email: Optional[str] = None
    owner_one_phone: Optional[str] = None
    owner_one_mailing_address: Optional[str] = None
    owner_two_full_name: Optional[str] = None
    owner_two_email: Optional[str] = None
    owner_two_phone: Optional[str] = None
    owner_two_mailing_address: Optional[str] = None
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
