import bcrypt


def hash_password(password: str) -> str:
    """Erzeugt einen bcrypt-Hash inkl. Salt (Anforderung 3)."""
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")


def check_password(password: str, password_hash: str) -> bool:
    """Vergleicht ein Klartext-Passwort mit einem gespeicherten Hash."""
    return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))
