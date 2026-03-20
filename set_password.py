import os
import hashlib
from dotenv import load_dotenv

load_dotenv()


def get_db_connection():
    import psycopg2

    return psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
    )


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def set_password(email: str, new_password: str) -> tuple[bool, str]:
    """Set the password for a user identified by email.

    Returns (ok, message).
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("UPDATE users SET password = %s WHERE email = %s RETURNING user_id", (hash_password(new_password), email))
        r = cur.fetchone()
        if not r:
            cur.close(); conn.close()
            return False, "No user found with that email."
        conn.commit()
        cur.close(); conn.close()
        return True, "Password updated successfully."
    except Exception as e:
        return False, f"DB error: {e}"


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Set a user's password in the users table")
    parser.add_argument("email", help="User email")
    parser.add_argument("password", help="New password")
    args = parser.parse_args()

    ok, msg = set_password(args.email, args.password)
    if ok:
        print(msg)
    else:
        print(f"Error: {msg}")
