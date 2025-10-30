import os
import sqlite3
from pathlib import Path
from typing import Iterable, Dict, Any, List

DB_PATH = Path(os.getenv('OPS_LLM_DB', '.ops_llm.sqlite'))

SCHEMA = '''
CREATE TABLE IF NOT EXISTS docs (
  id INTEGER PRIMARY KEY,
  namespace TEXT,
  title TEXT,
  section_title TEXT,
  text TEXT,
  meta JSON
);
CREATE INDEX IF NOT EXISTS ix_docs_ns ON docs(namespace);
'''

class SqliteStore:
    def __init__(self, path: Path = DB_PATH):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._init()

    def _init(self):
        with sqlite3.connect(self.path) as con:
            con.executescript(SCHEMA)

    def upsert_rows(self, rows: Iterable[Dict[str, Any]]):
        with sqlite3.connect(self.path) as con:
            con.executemany(
                'INSERT INTO docs(namespace,title,section_title,text,meta) VALUES (?,?,?,?,?)',
                [(r.get('namespace'), r.get('title'), r.get('section_title'), r.get('text'), str(r.get('meta') or {})) for r in rows]
            )

    def fetch_namespace(self, namespace: str, limit: int = 1000) -> List[Dict[str, Any]]:
        with sqlite3.connect(self.path) as con:
            cur = con.execute('SELECT title, section_title, text FROM docs WHERE namespace=? LIMIT ?', (namespace, limit))
            cols = [c[0] for c in cur.description]
            return [dict(zip(cols, row)) for row in cur.fetchall()]
