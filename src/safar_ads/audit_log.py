"""Append-only audit log for every read, recommendation, write request,
Amazon response, old/new value and approval decision (Phase 2.4).

Backed by a local JSONL file by default. In production this should point
at durable, access-controlled storage - swap AuditLog(path=...) for a
database-backed implementation without changing call sites.
"""

from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

DEFAULT_LOG_PATH = Path(__file__).resolve().parents[2] / "data" / "audit_log.jsonl"


@dataclass(frozen=True)
class AuditEntry:
    timestamp: float
    action: str
    actor: str
    dry_run: bool
    old_value: Any = None
    new_value: Any = None
    idempotency_key: str | None = None
    approved: bool | None = None
    result: str = "pending"          # "pending" | "ok" | "blocked" | "error"
    reason: str | None = None
    extra: dict = field(default_factory=dict)


class AuditLog:
    def __init__(self, path: Path | None = None) -> None:
        self.path = path or DEFAULT_LOG_PATH
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def record(self, entry: AuditEntry) -> None:
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(entry), default=str) + "\n")

    def log(
        self,
        *,
        action: str,
        actor: str = "safar_ads_agent",
        dry_run: bool = True,
        old_value: Any = None,
        new_value: Any = None,
        idempotency_key: str | None = None,
        approved: bool | None = None,
        result: str = "pending",
        reason: str | None = None,
        **extra: Any,
    ) -> AuditEntry:
        entry = AuditEntry(
            timestamp=time.time(),
            action=action,
            actor=actor,
            dry_run=dry_run,
            old_value=old_value,
            new_value=new_value,
            idempotency_key=idempotency_key,
            approved=approved,
            result=result,
            reason=reason,
            extra=extra,
        )
        self.record(entry)
        return entry

    def read_all(self) -> list[dict]:
        if not self.path.exists():
            return []
        with self.path.open("r", encoding="utf-8") as f:
            return [json.loads(line) for line in f if line.strip()]
