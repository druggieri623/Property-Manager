# Property Manager (HOA)

Starter workspace for an 11-unit condo HOA property management application.

## What is included

- `backend/`: FastAPI + SQLite API for owners and service providers
- `frontend/`: React + TypeScript + Vite web app
- `.vscode/`: tasks and settings for running both apps in VS Code

## Domain assumptions (initial)

- HOA uses **Bluestone Bank** for finances
- Dues are currently collected by **check**
- Owners: up to 11 units
- Service providers: fewer than 20

## Quick start

### 1) Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend API: `http://127.0.0.1:8000`
OpenAPI docs: `http://127.0.0.1:8000/docs`

### 2) Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend app: `http://127.0.0.1:5173`

## API endpoints (initial)

- `GET /health`
- `GET /settings/bank`
- `GET /owners`
- `POST /owners`
- `GET /service-providers`
- `POST /service-providers`

## Import owners from Excel

If you have an Excel file with owner columns like `name`, `email`, `phone`, `unit`, run:

```bash
cd backend
source .venv/bin/activate
python import_owners.py /absolute/path/to/owners.xlsx
```

Optional sheet name:

```bash
python import_owners.py /absolute/path/to/owners.xlsx --sheet "Sheet1"
```

The importer upserts by unit number (creates new owners or updates existing ones).

## Import service providers from Excel

If you have a service provider spreadsheet, run:

```bash
cd backend
source .venv/bin/activate
python import_service_providers.py /absolute/path/to/service_providers.xlsx
```

Optional sheet name:

```bash
python import_service_providers.py /absolute/path/to/service_providers.xlsx --sheet "Sheet1"
```

Expected columns include company/vendor name (required), plus optional contact, email, phone, category, notes.

## Next requirement inputs you can provide

- Owner data fields (phones, emails, mailing address, occupant info, unit status)
- Service provider fields (licenses, insurance expiration, preferred contact)
- Dues workflow (monthly amount, due date, late fee policy, check reconciliation)
- Reporting needs (delinquency, vendor payment history, annual budget export)

## Git workflow (daily use)

From the project root:

```bash
git status
git pull
```

Stage and commit changes:

```bash
git add .
git commit -m "Describe your change"
```

Push to GitHub:

```bash
git push
```

First push for a new branch:

```bash
git push -u origin <branch-name>
```
