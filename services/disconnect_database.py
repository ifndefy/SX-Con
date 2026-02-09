from typing import Optional
import pyodbc
import utils.logger as log

def disconnect(
    *,
    connection: Optional[pyodbc.Connection] = None,
    cursor: Optional[pyodbc.Cursor] = None,
    commit: bool = False,
    rollback: bool = False,
) -> int:
    """
    Closes the given cursor (if any) and then the connection.
    - If `rollback` is True, issue a rollback before closing.
    - Else if `commit` is True (and autocommit is False), commit before closing.
    Returns 0 on success, -1 on error.
    """

    """
        :author(s): Kyle Valdez
        :purpose: disconnects db connection
        :return: none
    """
    try:
        # Close cursor first (safe even if already closed)
        if cursor is not None:
            try:
                cursor.close()
            except Exception as e:
                log.warning(f"error while closing cursor: {e}")

        # Then handle the connection
        if connection is None:
            return 0

        try:
            if rollback:
                connection.rollback()
            elif commit and not getattr(connection, "autocommit", False):
                connection.commit()
        except Exception as e:
            # If commit/rollback fails, still attempt to close
            log.warning(f"commit/rollback failed: {e}")

        try:
            connection.close()
        except Exception as e:
            log.error(f"error while closing connection: {e}")
            return -1

        return 0
    except Exception as e:
        log.error(f"Unexpected error during disconnect: {e}")
        return -1