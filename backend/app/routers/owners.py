from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ..database import get_session
from ..models import Owner
from ..schemas import OwnerCreate, OwnerUpdate

router = APIRouter(prefix="/owners", tags=["owners"])


@router.get("", response_model=List[Owner])
def list_owners(session: Session = Depends(get_session)):
    return session.exec(select(Owner).order_by(Owner.unit_number)).all()


@router.post("", response_model=Owner)
def create_owner(payload: OwnerCreate, session: Session = Depends(get_session)):
    existing_owner = session.exec(
        select(Owner).where(Owner.unit_number == payload.unit_number)
    ).first()
    if existing_owner is not None:
        raise HTTPException(status_code=409, detail="Unit number already exists")

    owner = Owner.model_validate(payload)
    session.add(owner)
    session.commit()
    session.refresh(owner)
    return owner


@router.put("/{owner_id}", response_model=Owner)
def update_owner(
    owner_id: int, payload: OwnerUpdate, session: Session = Depends(get_session)
):
    owner = session.get(Owner, owner_id)
    if owner is None:
        raise HTTPException(status_code=404, detail="Owner not found")

    existing_owner = session.exec(
        select(Owner).where(Owner.unit_number == payload.unit_number)
    ).first()
    if existing_owner is not None and existing_owner.id != owner_id:
        raise HTTPException(status_code=409, detail="Unit number already exists")

    owner_data = payload.model_dump()
    for key, value in owner_data.items():
        setattr(owner, key, value)

    session.add(owner)
    session.commit()
    session.refresh(owner)
    return owner


@router.delete("/{owner_id}")
def delete_owner(owner_id: int, session: Session = Depends(get_session)):
    owner = session.get(Owner, owner_id)
    if owner is None:
        raise HTTPException(status_code=404, detail="Owner not found")

    session.delete(owner)
    session.commit()
    return {"deleted": True}
