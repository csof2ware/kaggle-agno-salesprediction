import json
from pathlib import Path
from datetime import datetime, timezone

RUNTIME_DIR = Path(__file__).resolve().parent.parent.parent / "runtime"
RUNTIME_DIR.mkdir(parents=True, exist_ok=True)

TOKEN_FILE = RUNTIME_DIR / "ml_token_state.json"

def load_token_state():
    if not TOKEN_FILE.exists():
        return {}
    with open(TOKEN_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_token_state(data: dict):
    with open(TOKEN_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def is_token_expired(expires_at_iso: str) -> bool:
    if not expires_at_iso:
        return True
    expires_at = datetime.fromisoformat(expires_at_iso)
    now = datetime.now(timezone.utc)
    return now >= expires_at