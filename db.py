
import os
from typing import Any, Dict, Optional, Union
from sqlalchemy import create_engine, text
from sqlalchemy.sql.elements import TextClause
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()
POSTGRES_URL = os.getenv('POSTGRES_URL')
if not POSTGRES_URL:
    raise RuntimeError('POSTGRES_URL not set. Create a .env file based on .env.example')

# Create engine with pre_ping to avoid stale connections
engine = create_engine(POSTGRES_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine)

# Internal: accept either str or TextClause
QueryType = Union[str, TextClause]

def _prepare_query(query: QueryType) -> TextClause:
    """Return a TextClause from either string or TextClause input."""
    return query if isinstance(query, TextClause) else text(query)

# --- Simple helpers ---

def fetch_one(query: QueryType, params: Optional[Dict[str, Any]] = None):
    """
    Execute a SELECT and return the first row as a mapping (dict-like), or None.
    Accepts either a plain SQL string or a SQLAlchemy TextClause.
    """
    with engine.connect() as conn:
        q = _prepare_query(query)
        return conn.execute(q, params or {}).mappings().first()

def fetch_all(query: QueryType, params: Optional[Dict[str, Any]] = None):
    """
    Execute a SELECT and return all rows as a list of mappings (dict-like).
    Accepts either a plain SQL string or a SQLAlchemy TextClause.
    """
    with engine.connect() as conn:
        q = _prepare_query(query)
        return conn.execute(q, params or {}).mappings().all()

def fetch_scalar(query: QueryType, params: Optional[Dict[str, Any]] = None):
    """
    Execute a SELECT and return the first column of the first row (scalar), or None.
    Useful for existence checks and counts.
    """
    with engine.connect() as conn:
        q = _prepare_query(query)
        row = conn.execute(q, params or {}).first()
        return None if row is None else row[0]

def execute(query: QueryType, params: Optional[Dict[str, Any]] = None):
    """
    Execute an INSERT/UPDATE/DELETE (or DDL) within a transaction.
    Accepts either a plain SQL string or a SQLAlchemy TextClause.
    """
    with engine.begin() as conn:
        q = _prepare_query(query)
        conn.execute(q, params or {})
