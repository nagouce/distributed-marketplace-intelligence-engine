import sqlite3
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger("STORAGE")

class DatabaseManager:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self.db_path), timeout=15)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        schema_path = Path(__file__).resolve().parents[2] / "sql" / "schema.sql"
        if schema_path.exists():
            with self.get_connection() as conn:
                with open(schema_path, "r", encoding="utf-8") as f:
                    conn.executescript(f.read())
                conn.commit()
            logger.info("Database schema initialized successfully.")

    def get_pending_count(self, date_str: str) -> int:
        query = "SELECT COUNT(*) FROM fila_postagem WHERE status = 'pendente' AND data_fila = ?"
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (date_str,))
                row = cursor.fetchone()
                return row[0] if row else 0
        except sqlite3.Error as e:
            logger.error(f"Failed to fetch pending queue count: {e}", exc_info=True)
            return 0
