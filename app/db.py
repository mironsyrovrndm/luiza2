from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker

engine = None
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, future=True))
Base = declarative_base()


def init_engine(database_url: str) -> None:
    global engine
    engine = create_engine(database_url, pool_pre_ping=True, future=True)
    SessionLocal.configure(bind=engine)


def get_session():
    return SessionLocal()


@contextmanager
def session_scope():
    session = get_session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
