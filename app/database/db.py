import os
from sqlalchemy import create_engine, Column, String, MetaData, Table
from sqlalchemy.orm import declarative_base, sessionmaker

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

DB_PATH = os.path.join(BASE_DIR, "ticketing.db")
DB_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()
metadata = MetaData()

# Declarative model used by Flask-Login and auth routes
class User(Base):
    __tablename__ = "users"

    user_id        = Column(String, primary_key=True)
    password       = Column(String, nullable=False)
    short_username = Column(String, unique=True, nullable=False)
    full_name      = Column(String, nullable=False)

    # ── Flask-Login required interface ──────────────────────────────
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.user_id
