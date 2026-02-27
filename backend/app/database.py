import sqlite3
from pathlib import Path

from sqlmodel import Session, SQLModel, create_engine

DB_PATH = Path(__file__).resolve().parent.parent / "hoa.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


def migrate_owner_schema_for_two_owners() -> None:
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()
        cursor.execute("PRAGMA table_info(owner)")
        columns = cursor.fetchall()
        if not columns:
            return

        existing_column_names = {column[1] for column in columns}
        required_columns = [
            "owner_one_full_name",
            "owner_one_email",
            "owner_one_phone",
            "owner_one_mailing_address",
            "owner_two_full_name",
            "owner_two_email",
            "owner_two_phone",
            "owner_two_mailing_address",
        ]

        for column_name in required_columns:
            if column_name not in existing_column_names:
                cursor.execute(f"ALTER TABLE owner ADD COLUMN {column_name} TEXT")

        legacy_full_name_column = (
            "full_name" if "full_name" in existing_column_names else "owner_one_full_name"
        )
        legacy_email_column = "email" if "email" in existing_column_names else "owner_one_email"
        legacy_phone_column = "phone" if "phone" in existing_column_names else "owner_one_phone"
        legacy_mailing_column = (
            "mailing_address"
            if "mailing_address" in existing_column_names
            else "owner_one_mailing_address"
        )

        cursor.execute(
            f"""
            UPDATE owner
            SET
                owner_one_full_name = COALESCE(owner_one_full_name, {legacy_full_name_column}, ''),
                owner_one_email = COALESCE(owner_one_email, {legacy_email_column}),
                owner_one_phone = COALESCE(owner_one_phone, {legacy_phone_column}),
                owner_one_mailing_address = COALESCE(owner_one_mailing_address, {legacy_mailing_column})
            """
        )

        cursor.execute(
            f"""
            SELECT
                id,
                {legacy_full_name_column} AS legacy_full_name,
                {legacy_email_column} AS legacy_email,
                {legacy_phone_column} AS legacy_phone,
                owner_one_full_name,
                owner_one_email,
                owner_one_phone,
                owner_two_full_name,
                owner_two_email,
                owner_two_phone
            FROM owner
            """
        )
        rows = cursor.fetchall()

        for row in rows:
            owner_id = row[0]
            legacy_name = row[1] or ""
            legacy_email = row[2] or ""
            legacy_phone = row[3] or ""

            owner_one_name = row[4]
            owner_one_email = row[5]
            owner_one_phone = row[6]
            owner_two_name = row[7]
            owner_two_email = row[8]
            owner_two_phone = row[9]

            name_parts = [part.strip() for part in legacy_name.splitlines() if part.strip()]
            email_parts = [part.strip() for part in legacy_email.splitlines() if part.strip()]
            phone_parts = [part.strip() for part in legacy_phone.splitlines() if part.strip()]

            if len(name_parts) > 1 and not owner_two_name:
                owner_two_name = name_parts[1]
            if len(name_parts) > 1:
                owner_one_name = name_parts[0]

            if len(email_parts) > 1 and not owner_two_email:
                owner_two_email = email_parts[1]
            if len(email_parts) > 1:
                owner_one_email = email_parts[0]

            if len(phone_parts) > 1 and not owner_two_phone:
                owner_two_phone = phone_parts[1]
            if len(phone_parts) > 1:
                owner_one_phone = phone_parts[0]

            cursor.execute(
                """
                UPDATE owner
                SET
                    owner_one_full_name = ?,
                    owner_one_email = ?,
                    owner_one_phone = ?,
                    owner_two_full_name = ?,
                    owner_two_email = ?,
                    owner_two_phone = ?
                WHERE id = ?
                """,
                (
                    owner_one_name,
                    owner_one_email,
                    owner_one_phone,
                    owner_two_name,
                    owner_two_email,
                    owner_two_phone,
                    owner_id,
                ),
            )
        connection.commit()


def get_session():
    with Session(engine) as session:
        yield session
