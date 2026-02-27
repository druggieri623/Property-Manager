from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select

from .database import create_db_and_tables, engine, get_session
from .models import DuesPaymentMethod, HOASetting, Owner, ServiceProvider
from .routers.owners import router as owners_router
from .routers.service_providers import router as service_providers_router

app = FastAPI(title="HOA Property Manager API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


DEFAULT_OWNERS = [
    {"unit_number": "1", "full_name": "Owner Unit 1"},
    {"unit_number": "2", "full_name": "Owner Unit 2"},
    {"unit_number": "3", "full_name": "Owner Unit 3"},
    {"unit_number": "4", "full_name": "Owner Unit 4"},
    {"unit_number": "5", "full_name": "Owner Unit 5"},
    {"unit_number": "6", "full_name": "Owner Unit 6"},
    {"unit_number": "7", "full_name": "Owner Unit 7"},
    {"unit_number": "8", "full_name": "Owner Unit 8"},
    {"unit_number": "9", "full_name": "Owner Unit 9"},
    {"unit_number": "10", "full_name": "Owner Unit 10"},
    {"unit_number": "11", "full_name": "Owner Unit 11"},
]

DEFAULT_SERVICE_PROVIDERS = [
    {
        "company_name": "ClearView Plumbing",
        "contact_name": "Jordan Hayes",
        "phone": "555-0101",
        "service_category": "Plumbing",
    },
    {
        "company_name": "Summit Electrical",
        "contact_name": "Avery Cole",
        "phone": "555-0102",
        "service_category": "Electrical",
    },
    {
        "company_name": "Greenline Landscaping",
        "contact_name": "Taylor Reed",
        "phone": "555-0103",
        "service_category": "Landscaping",
    },
]


def seed_initial_data() -> None:
    with Session(engine) as session:
        settings = session.get(HOASetting, 1)
        if settings is None:
            settings = HOASetting(id=1, bank_name="Bluestone Bank")
            session.add(settings)

        owner_count = len(session.exec(select(Owner.id)).all())
        if owner_count == 0:
            for owner_seed in DEFAULT_OWNERS:
                session.add(
                    Owner(
                        unit_number=owner_seed["unit_number"],
                        full_name=owner_seed["full_name"],
                        dues_payment_method=DuesPaymentMethod.CHECK,
                    )
                )

        provider_count = len(session.exec(select(ServiceProvider.id)).all())
        if provider_count == 0:
            for provider_seed in DEFAULT_SERVICE_PROVIDERS:
                session.add(ServiceProvider(**provider_seed))

        session.commit()


@app.on_event("startup")
def on_startup() -> None:
    create_db_and_tables()
    seed_initial_data()


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/settings/bank")
def get_bank_setting(session: Session = Depends(get_session)):
    settings = session.exec(select(HOASetting).where(HOASetting.id == 1)).first()
    if settings is None:
        settings = HOASetting(bank_name="Bluestone Bank")
        session.add(settings)
        session.commit()
        session.refresh(settings)
    return {"bank_name": settings.bank_name, "dues_collection_method": "check"}


app.include_router(owners_router)
app.include_router(service_providers_router)
