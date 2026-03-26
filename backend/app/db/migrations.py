from sqlalchemy import inspect, text
from sqlalchemy.engine import Engine


def apply_safe_schema_updates(engine: Engine) -> None:
    inspector = inspect(engine)
    tables = set(inspector.get_table_names())
    if "resumes" not in tables:
        return

    existing_columns = {column["name"] for column in inspector.get_columns("resumes")}
    statements: list[str] = []

    if "target_title" not in existing_columns:
        statements.append("ALTER TABLE resumes ADD COLUMN target_title VARCHAR(200)")
    if "target_location" not in existing_columns:
        statements.append("ALTER TABLE resumes ADD COLUMN target_location VARCHAR(120)")

    if not statements:
        return

    with engine.begin() as connection:
        for statement in statements:
            connection.execute(text(statement))
