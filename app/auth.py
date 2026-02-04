from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from app.db import session_scope
from app.models import AdminUser

password_hasher = PasswordHasher()


def verify_password(password: str, password_hash: str) -> bool:
    try:
        return password_hasher.verify(password_hash, password)
    except VerifyMismatchError:
        return False


def hash_password(password: str) -> str:
    return password_hasher.hash(password)


def get_admin_by_username(username: str) -> AdminUser | None:
    with session_scope() as session:
        return session.query(AdminUser).filter_by(username=username).one_or_none()
