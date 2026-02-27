from typing import Optional

from pydantic import BaseModel

from .models import DuesPaymentMethod


class OwnerCreate(BaseModel):
    unit_number: str
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


class OwnerUpdate(BaseModel):
    unit_number: str
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
