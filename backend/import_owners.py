from __future__ import annotations

import argparse
from pathlib import Path

from openpyxl import load_workbook
from sqlmodel import Session, select

from app.database import engine
from app.models import DuesPaymentMethod, Owner


def normalize_header(value: object) -> str:
    if value is None:
        return ""
    return "".join(ch for ch in str(value).strip().lower() if ch.isalnum())


def normalize_value(value: object) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text if text else None


def map_headers(header_row: tuple[object, ...]) -> dict[str, int]:
    aliases = {
        "unit": "unit",
        "unitnumber": "unit",
        "unit#": "unit",
        "name": "name",
        "ownername": "name",
        "ownersname": "name",
        "fullname": "name",
        "email": "email",
        "emailaddress": "email",
        "phone": "phone",
        "phonenumber": "phone",
    }
    mapped: dict[str, int] = {}
    for index, cell in enumerate(header_row):
        canonical = aliases.get(normalize_header(cell))
        if canonical is not None and canonical not in mapped:
            mapped[canonical] = index
    missing = [required for required in ("unit", "name") if required not in mapped]
    if missing:
        raise ValueError(
            f"Missing required columns: {', '.join(missing)}. "
            "Expected headers like unit, name, email, phone."
        )
    return mapped


def find_header_row(rows: list[tuple[object, ...]]) -> tuple[int, dict[str, int]]:
    max_scan = min(len(rows), 20)
    for index in range(max_scan):
        try:
            header_map = map_headers(rows[index])
            return index, header_map
        except ValueError:
            continue
    raise ValueError(
        "Could not detect header row with required columns. "
        "Expected columns like unit and owner name."
    )


def import_owners(file_path: Path, sheet_name: str | None) -> tuple[int, int, int]:
    workbook = load_workbook(filename=file_path, data_only=True)
    sheet = workbook[sheet_name] if sheet_name else workbook.active

    rows = list(sheet.iter_rows(values_only=True))
    if not rows:
        raise ValueError("Spreadsheet is empty")

    header_row_index, header_map = find_header_row(rows)
    created = 0
    updated = 0
    skipped = 0

    with Session(engine) as session:
        for row in rows[header_row_index + 1 :]:
            unit = normalize_value(row[header_map["unit"]])
            name = normalize_value(row[header_map["name"]])
            email = (
                normalize_value(row[header_map["email"]])
                if "email" in header_map
                else None
            )
            phone = (
                normalize_value(row[header_map["phone"]])
                if "phone" in header_map
                else None
            )

            if unit is None or name is None:
                skipped += 1
                continue

            existing = session.exec(
                select(Owner).where(Owner.unit_number == unit)
            ).first()
            if existing is None:
                owner = Owner(
                    unit_number=unit,
                    full_name=name,
                    email=email,
                    phone=phone,
                    dues_payment_method=DuesPaymentMethod.CHECK,
                    active=True,
                )
                session.add(owner)
                created += 1
            else:
                existing.full_name = name
                existing.email = email
                existing.phone = phone
                session.add(existing)
                updated += 1

        session.commit()

    return created, updated, skipped


def main() -> None:
    parser = argparse.ArgumentParser(description="Import owner data from an Excel file")
    parser.add_argument("excel_file", help="Absolute or relative path to .xlsx file")
    parser.add_argument("--sheet", default=None, help="Optional sheet name")
    args = parser.parse_args()

    file_path = Path(args.excel_file).expanduser().resolve()
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    created, updated, skipped = import_owners(
        file_path=file_path, sheet_name=args.sheet
    )
    print(
        "Owner import complete "
        f"(created={created}, updated={updated}, skipped={skipped})"
    )


if __name__ == "__main__":
    main()
