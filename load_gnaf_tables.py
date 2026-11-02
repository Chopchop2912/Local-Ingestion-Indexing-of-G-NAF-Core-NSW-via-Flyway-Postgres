from pathlib import Path
import psycopg

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "address_sandbox",
    "user": "postgres",
    "password": "12345"
}

ROOT = Path(r"C:\Users\Justin.Lam\Desktop\GNAFAUGUST2026")

AUTHORITY_DIR = ROOT / "Authority Code"
STANDARD_DIR = ROOT / "Standard"

STATE_PREFIXES = {
    "ACT",
    "NSW",
    "NT",
    "OT",
    "QLD",
    "SA",
    "TAS",
    "VIC",
    "WA"
}


def authority_table_name(file_name: str) -> str:
    return (
        file_name
        .replace("Authority_Code_", "")
        .replace("_psv.psv", "")
    )


def state_table_name(file_name: str) -> str:
    parts = file_name.replace("_psv.psv", "").split("_")

    state = parts[0]

    if state not in STATE_PREFIXES:
        raise ValueError(f"Unexpected state prefix: {state}")

    return "_".join(parts[1:])


def copy_file(conn, table_name: str, file_path: Path):
    print(f"Loading {file_path.name} -> {table_name}")

    sql = f"""
    COPY {table_name}
    FROM STDIN
    WITH (
        FORMAT csv,
        DELIMITER '|',
        HEADER true
    )
    """

    with conn.cursor() as cur:
        with open(file_path, "r", encoding="utf-8") as f:
            with cur.copy(sql) as copy:
                while data := f.read(1024 * 1024):
                    copy.write(data)

    conn.commit()


def main():
    conn = psycopg.connect(**DB_CONFIG)

    try:
        for file in sorted(AUTHORITY_DIR.glob("*.psv")):
            table = authority_table_name(file.name)
            copy_file(conn, table, file)

        for file in sorted(STANDARD_DIR.glob("*.psv")):
            table = state_table_name(file.name)
            copy_file(conn, table, file)

        print("Load complete")

    finally:
        conn.close()


if __name__ == "__main__":
    main()