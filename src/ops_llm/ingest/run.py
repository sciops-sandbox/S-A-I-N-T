import json
from pathlib import Path
from typing import Dict, Any, List
import yaml

from src.ops_llm.store.sqlite_store import SqliteStore
from src.ops_llm.text.chunk import split_text, extract_text_from_path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

def load_cfg(path: Path) -> Dict[str, Any]:
    return yaml.safe_load(path.read_text())

def run(cfg_path: str = 'config/sources.yaml', namespace: str = 'default'):
    cfg = load_cfg(Path(cfg_path))
    store = SqliteStore()
    rows = []
    for src in cfg.get('sources', []):
        if src.get('type') == 'filesystem':
            for base in src.get('paths', []):
                base = Path(base)
                for pattern in src.get('include', ['**/*']):
                    for path in base.glob(pattern):
                        text = extract_text_from_path(path)
                        if not text:
                            continue
                        for chunk in split_text(text, **cfg.get('chunking', {})):
                            rows.append({
                                'namespace': namespace,
                                'title': path.name,
                                'section_title': 'auto',
                                'text': chunk,
                                'meta': {'path': str(path)}
                            })
    if rows:
        store.upsert_rows(rows)
        print(f'Inserted {len(rows)} rows into {store.path}')
    else:
        print('No rows ingested. Check your config and input paths.')

if __name__ == '__main__':
    run()
