from typing import Optional

from pydantic import BaseModel

from .models import DuesPaymentMethod


class OwnerCreate(BaseModel):
    unit_number: str
    full_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    mailing_address: Optional[str] = None
    dues_payment_method: DuesPaymentMethod = DuesPaymentMethod.CHECK
    active: bool = True


class OwnerUpdate(BaseModel):
    unit_number: str
    full_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    mailing_address: Optional[str] = None
    dues_payment_method: DuesPaymentMethod = DuesPaymentMethod.CHECK
    active: bool = True


class ServiceProviderCreate(BaseModel):
    company_name: str
    contact_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    service_category: Optional[str] = None
    notes: Optional[str] = None
    active: bool = True


class ServiceProviderUpdate(BaseModel):
    company_name: str
    contact_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    service_category: Optional[str] = None
    notes: Optional[str] = None
    active: bool = True
