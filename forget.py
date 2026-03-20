import os
import hashlib
import secrets
from datetime import datetime, timedelta
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


def password_reset_table_exists() -> bool:
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT to_regclass('public.password_reset')")
        row = cur.fetchone()
        cur.close(); conn.close()
        return bool(row and row[0])
    except Exception:
        return False


def create_reset_code(email: str, ttl_minutes: int = 15) -> str | None:
    """Create a short numeric reset code and store it in `password_reset` if the table exists.
    Returns the code (caller should email it to user). If table doesn't exist, returns None.
    """
    if not password_reset_table_exists():
        return None

    code = f"{secrets.randbelow(1000000):06d}"
    expires = datetime.utcnow() + timedelta(minutes=ttl_minutes)
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM password_reset WHERE email = %s", (email,))
        cur.execute(
            "INSERT INTO password_reset (email, code, expires_at) VALUES (%s, %s, %s)",
            (email, code, expires),
        )
        conn.commit()
        cur.close(); conn.close()
        return code
    except Exception:
        return None


def verify_code_and_set_password(email: str, code: str, new_password: str) -> tuple[bool, str]:
    """Verify a reset code and update the user's password if valid.
    Returns (ok, message).
    If `password_reset` table doesn't exist, returns (False, message).
    """
    if not password_reset_table_exists():
        return False, "Password reset table not present in DB. Contact admin to reset password."

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT code, expires_at FROM password_reset WHERE email = %s ORDER BY created_at DESC LIMIT 1",
            (email,),
        )
        row = cur.fetchone()
        if not row:
            cur.close(); conn.close()
            return False, "No reset request found for that email."

        stored_code, expires_at = row
        if stored_code != code:
            cur.close(); conn.close()
            return False, "Invalid code."
        if expires_at is None or expires_at < datetime.utcnow():
            cur.close(); conn.close()
            return False, "Code expired. Please request a new reset code."

        # update password
        cur.execute("UPDATE users SET password = %s WHERE email = %s RETURNING user_id", (hash_password(new_password), email))
        urow = cur.fetchone()
        if not urow:
            cur.close(); conn.close()
            return False, "No user found with that email."

        # cleanup
        cur.execute("DELETE FROM password_reset WHERE email = %s", (email,))
        conn.commit()
        cur.close(); conn.close()
        return True, "Password updated successfully."
    except Exception as e:
        return False, f"DB error: {e}"


def force_set_password(email: str, new_password: str) -> tuple[bool, str]:
    """Directly set a user's password (admin operation)."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("UPDATE users SET password = %s WHERE email = %s RETURNING user_id", (hash_password(new_password), email))
        r = cur.fetchone()
        if not r:
            cur.close(); conn.close()
            return False, "No user with that email."
        conn.commit()
        cur.close(); conn.close()
        return True, "Password updated (admin)."
    except Exception as e:
        return False, f"DB error: {e}"


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Password reset helper for PulsePlay")
    sub = parser.add_subparsers(dest="cmd")

    req = sub.add_parser("request", help="Create a reset code for an email (prints code).")
    req.add_argument("email")

    reset = sub.add_parser("reset", help="Reset password using code")
    reset.add_argument("email")
    reset.add_argument("code")
    reset.add_argument("new_password")

    force = sub.add_parser("force", help="Force-set password for email (admin)")
    force.add_argument("email")
    force.add_argument("new_password")

    args = parser.parse_args()
    if args.cmd == "request":
        code = create_reset_code(args.email)
        if code:
            print(f"Reset code for {args.email}: {code} (valid for 15 minutes)")
        else:
            print("Could not create reset code. Make sure `password_reset` table exists in DB.")
    elif args.cmd == "reset":
        ok, msg = verify_code_and_set_password(args.email, args.code, args.new_password)
        print(msg)
    elif args.cmd == "force":
        ok, msg = force_set_password(args.email, args.new_password)
        print(msg)
    else:
        parser.print_help()
