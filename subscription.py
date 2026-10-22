"""PRO жазылым мерзімі (оқушыға көрсетілмейді).

SUPABASE_URL + SUPABASE_SERVICE_ROLE_KEY болса — Postgres.
Әйтпесе жергілікті SQLite (data/subscriptions.db).
"""

from __future__ import annotations

import logging
import os
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path

log = logging.getLogger(__name__)

STATUS_ACTIVE = "active"
STATUS_EXPIRED = "expired"
SUBSCRIPTION_DAYS = 30

_DB_PATH = Path(__file__).resolve().parent / "data" / "subscriptions.db"


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).replace(microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")


def _supabase_configured() -> bool:
    return bool(os.getenv("SUPABASE_URL", "").strip() and os.getenv("SUPABASE_SERVICE_ROLE_KEY", "").strip())


def _connect_sqlite() -> sqlite3.Connection:
    _DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(_DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS subscriptions (
            telegram_id INTEGER PRIMARY KEY,
            status TEXT NOT NULL DEFAULT 'active',
            paid_at TEXT,
            expires_at TEXT,
            reminder_sent INTEGER NOT NULL DEFAULT 0
        )
        """
    )
    conn.execute(
        "CREATE INDEX IF NOT EXISTS subscriptions_expiry_idx "
        "ON subscriptions (status, expires_at, reminder_sent)"
    )
    conn.commit()
    return conn


def activate_subscription(telegram_id: int) -> None:
    """Төлем расталғанда: 30 күн, status=active, reminder_sent=false."""
    now = _now()
    payload = {
        "telegram_id": telegram_id,
        "status": STATUS_ACTIVE,
        "paid_at": _iso(now),
        "expires_at": _iso(now + timedelta(days=SUBSCRIPTION_DAYS)),
        "reminder_sent": False,
    }
    if _supabase_configured():
        _supabase_upsert(payload)
    else:
        _sqlite_upsert(payload)
    log.info("Жазылым жаңартылды: user=%s expires=%s", telegram_id, payload["expires_at"])


def due_reminders() -> list[int]:
    """expires_at-қа 24 сағаттан аз қалған, әлі ескертілмеген active қолданушылар."""
    now = _now()
    until = now + timedelta(hours=24)
    if _supabase_configured():
        rows = _supabase_select(
            {
                "status": f"eq.{STATUS_ACTIVE}",
                "reminder_sent": "eq.false",
                "and": f"(expires_at.gt.{_iso(now)},expires_at.lte.{_iso(until)})",
            }
        )
        return [int(r["telegram_id"]) for r in rows]
    with _connect_sqlite() as conn:
        rows = conn.execute(
            """
            SELECT telegram_id FROM subscriptions
            WHERE status = ?
              AND reminder_sent = 0
              AND expires_at > ?
              AND expires_at <= ?
            """,
            (STATUS_ACTIVE, _iso(now), _iso(until)),
        ).fetchall()
        return [int(r["telegram_id"]) for r in rows]


def mark_reminder_sent(telegram_id: int) -> None:
    if _supabase_configured():
        _supabase_update(telegram_id, {"reminder_sent": True})
        return
    with _connect_sqlite() as conn:
        conn.execute(
            "UPDATE subscriptions SET reminder_sent = 1 WHERE telegram_id = ?",
            (telegram_id,),
        )
        conn.commit()


def due_expirations() -> list[int]:
    """Мерзімі біткен, әлі active тұрған қолданушылар."""
    now = _now()
    if _supabase_configured():
        rows = _supabase_select(
            {
                "status": f"eq.{STATUS_ACTIVE}",
                "expires_at": f"lte.{_iso(now)}",
            }
        )
        return [int(r["telegram_id"]) for r in rows]
    with _connect_sqlite() as conn:
        rows = conn.execute(
            """
            SELECT telegram_id FROM subscriptions
            WHERE status = ? AND expires_at <= ?
            """,
            (STATUS_ACTIVE, _iso(now)),
        ).fetchall()
        return [int(r["telegram_id"]) for r in rows]


def is_subscription_active(telegram_id: int) -> bool:
    """Төлем расталған және мерзімі бітпеген қолданушы ма."""
    now = _iso(_now())
    if _supabase_configured():
        rows = _supabase_select(
            {
                "telegram_id": f"eq.{telegram_id}",
                "status": f"eq.{STATUS_ACTIVE}",
                "expires_at": f"gt.{now}",
            }
        )
        return bool(rows)
    with _connect_sqlite() as conn:
        row = conn.execute(
            """
            SELECT 1 FROM subscriptions
            WHERE telegram_id = ? AND status = ? AND expires_at > ?
            LIMIT 1
            """,
            (telegram_id, STATUS_ACTIVE, now),
        ).fetchone()
        return row is not None


def mark_expired(telegram_id: int) -> None:
    if _supabase_configured():
        _supabase_update(telegram_id, {"status": STATUS_EXPIRED})
        return
    with _connect_sqlite() as conn:
        conn.execute(
            "UPDATE subscriptions SET status = ? WHERE telegram_id = ?",
            (STATUS_EXPIRED, telegram_id),
        )
        conn.commit()


def _sqlite_upsert(payload: dict) -> None:
    with _connect_sqlite() as conn:
        conn.execute(
            """
            INSERT INTO subscriptions (telegram_id, status, paid_at, expires_at, reminder_sent)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(telegram_id) DO UPDATE SET
                status = excluded.status,
                paid_at = excluded.paid_at,
                expires_at = excluded.expires_at,
                reminder_sent = excluded.reminder_sent
            """,
            (
                payload["telegram_id"],
                payload["status"],
                payload["paid_at"],
                payload["expires_at"],
                1 if payload["reminder_sent"] else 0,
            ),
        )
        conn.commit()


def _supabase_headers() -> dict[str, str]:
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "").strip()
    return {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal",
    }


def _supabase_upsert(payload: dict) -> None:
    import urllib.error
    import urllib.request
    import json

    url = os.getenv("SUPABASE_URL", "").rstrip("/") + "/rest/v1/subscriptions"
    body = json.dumps({**payload, "reminder_sent": bool(payload["reminder_sent"])}).encode()
    headers = _supabase_headers()
    headers["Prefer"] = "resolution=merge-duplicates,return=minimal"
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            resp.read()
    except urllib.error.HTTPError as exc:
        log.error("Supabase upsert қатесі: %s %s", exc.code, exc.read().decode("utf-8", errors="replace"))
        raise


def _supabase_update(telegram_id: int, fields: dict) -> None:
    import urllib.error
    import urllib.request
    import json

    url = (
        os.getenv("SUPABASE_URL", "").rstrip("/")
        + f"/rest/v1/subscriptions?telegram_id=eq.{telegram_id}"
    )
    body = json.dumps(fields).encode()
    req = urllib.request.Request(url, data=body, headers=_supabase_headers(), method="PATCH")
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            resp.read()
    except urllib.error.HTTPError as exc:
        log.error("Supabase update қатесі: %s %s", exc.code, exc.read().decode("utf-8", errors="replace"))
        raise


def _supabase_select(params: dict[str, str]) -> list[dict]:
    import urllib.error
    import urllib.parse
    import urllib.request
    import json

    query = urllib.parse.urlencode(params)
    url = os.getenv("SUPABASE_URL", "").rstrip("/") + f"/rest/v1/subscriptions?select=telegram_id&{query}"
    req = urllib.request.Request(url, headers=_supabase_headers(), method="GET")
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as exc:
        log.error("Supabase select қатесі: %s %s", exc.code, exc.read().decode("utf-8", errors="replace"))
        raise
