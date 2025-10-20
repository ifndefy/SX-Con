# services/disconnectDB.py
"""
Facade to manage disconnecting from the database and preventing any
future use after a disconnect.

- Lives in disconnectDB.py (per story)
- Returns 0 on success, -1 on error
- After disconnect, any attempt to get/use a connection raises an error
  so a plain SELECT fails as required.
"""

from __future__ import annotations

from typing import Optional

# Import your DatabaseConnection the same way your service does
try:
    # If this file is inside services/ alongside connectDB.py
    from services import connectDB as db
except ImportError:
    # If used from the same folder
    import connectDB as db  # type: ignore


# --- Module-level state ------------------------------------------------------

_CONN: Optional[db.DatabaseConnection] = None
_DB_DISABLED: bool = False


# --- Public API --------------------------------------------------------------

def get_connection() -> db.DatabaseConnection:
    """
    Return a shared DatabaseConnection. Lazily establishes the connection
    unless the DB has been disabled via disconnect_db().

    Raises:
        RuntimeError: if database access has been disabled or if establishing
                      the connection fails.
    """
    global _CONN, _DB_DISABLED

    if _DB_DISABLED:
        raise RuntimeError("Database access disabled")

    if _CONN is None:
        _CONN = db.DatabaseConnection()
        rc = _CONN.establish_connection()
        if rc != 0:
            _CONN = None
            raise RuntimeError("Failed to establish database connection")

    return _CONN


def disconnect_db() -> int:
    """
    Close the active connection (if any) and permanently disable future DB use.

    Returns:
        int: 0 on success; -1 on any error (per acceptance criteria).
    """
    global _CONN, _DB_DISABLED

    try:
        if _CONN is not None:
            # Your class already knows how to close safely
            _CONN.close_connection()
        _CONN = None
        _DB_DISABLED = True
        return 0
    except Exception:
        # Still disable to ensure future SELECTs fail, and signal error
        _CONN = None
        _DB_DISABLED = True
        return -1


def is_disabled() -> bool:
    """True if disconnect_db() has been called and DB access is blocked."""
    return _DB_DISABLED


def execute(sql: str, *params):
    """
    Optional convenience for simple checks/QA:
    Execute a query using the shared connection. After disconnect_db()
    this will raise RuntimeError, ensuring a 'SELECT ...' fails.

    Returns:
        Fetched rows (driver dependent) on success.

    Raises:
        RuntimeError: if DB is disabled or connection isn't established.
        Exception:    if the underlying cursor.execute() fails.
    """
    if _DB_DISABLED:
        raise RuntimeError("Database access disabled")

    conn = get_connection()
    cur = conn.create_cursor()
    try:
        if params:
            cur.execute(sql, params)
        else:
            cur.execute(sql)
        try:
            return cur.fetchall()
        except Exception:
            # Not all statements return rows
            return None
    finally:
        try:
            cur.close()
        except Exception:
            pass
