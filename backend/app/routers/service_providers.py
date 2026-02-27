from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ..database import get_session
from ..models import ServiceProvider
from ..schemas import ServiceProviderCreate, ServiceProviderUpdate

router = APIRouter(prefix="/service-providers", tags=["service-providers"])


@router.get("", response_model=List[ServiceProvider])
def list_service_providers(session: Session = Depends(get_session)):
    return session.exec(
        select(ServiceProvider).order_by(ServiceProvider.company_name)
    ).all()


@router.post("", response_model=ServiceProvider)
def create_service_provider(
    payload: ServiceProviderCreate, session: Session = Depends(get_session)
):
    existing_provider = session.exec(
        select(ServiceProvider).where(
            ServiceProvider.company_name == payload.company_name
        )
    ).first()
    if existing_provider is not None:
        raise HTTPException(status_code=409, detail="Company name already exists")

    provider = ServiceProvider.model_validate(payload)
    session.add(provider)
    session.commit()
    session.refresh(provider)
    return provider


@router.put("/{provider_id}", response_model=ServiceProvider)
def update_service_provider(
    provider_id: int,
    payload: ServiceProviderUpdate,
    session: Session = Depends(get_session),
):
    provider = session.get(ServiceProvider, provider_id)
    if provider is None:
        raise HTTPException(status_code=404, detail="Service provider not found")

    existing_provider = session.exec(
        select(ServiceProvider).where(
            ServiceProvider.company_name == payload.company_name
        )
    ).first()
    if existing_provider is not None and existing_provider.id != provider_id:
        raise HTTPException(status_code=409, detail="Company name already exists")

    provider_data = payload.model_dump()
    for key, value in provider_data.items():
        setattr(provider, key, value)

    session.add(provider)
    session.commit()
    session.refresh(provider)
    return provider


@router.delete("/{provider_id}")
def delete_service_provider(provider_id: int, session: Session = Depends(get_session)):
    provider = session.get(ServiceProvider, provider_id)
    if provider is None:
        raise HTTPException(status_code=404, detail="Service provider not found")

    session.delete(provider)
    session.commit()
    return {"deleted": True}
