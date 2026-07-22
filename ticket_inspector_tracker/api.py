from __future__ import annotations

import json
import threading
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any
from urllib.parse import parse_qs, urlparse


@dataclass
class Sighting:
    id: int
    line: str
    stop: str
    direction: str | None
    inspector_count: int
    reported_at: str


class SightingStore:
    def __init__(self) -> None:
        self._items: list[Sighting] = []
        self._next_id = 1
        self._lock = threading.Lock()

    def add(self, payload: dict[str, Any]) -> Sighting:
        line = payload.get("line")
        stop = payload.get("stop")
        direction = payload.get("direction")
        inspector_count = payload.get("inspector_count", 1)

        if not isinstance(line, str) or not line.strip():
            raise ValueError("line is required and must be a non-empty string")
        if not isinstance(stop, str) or not stop.strip():
            raise ValueError("stop is required and must be a non-empty string")
        if direction is not None and not isinstance(direction, str):
            raise ValueError("direction must be a string when provided")
        if not isinstance(inspector_count, int) or inspector_count < 1:
            raise ValueError("inspector_count must be an integer greater than 0")

        with self._lock:
            sighting = Sighting(
                id=self._next_id,
                line=line.strip(),
                stop=stop.strip(),
                direction=direction.strip() if isinstance(direction, str) and direction.strip() else None,
                inspector_count=inspector_count,
                reported_at=datetime.now(timezone.utc).isoformat(),
            )
            self._items.append(sighting)
            self._next_id += 1
            return sighting

    def list(self, line: str | None = None) -> list[Sighting]:
        with self._lock:
            items = list(self._items)

        if line:
            target = line.strip().lower()
            items = [item for item in items if item.line.lower() == target]

        items.sort(key=lambda item: item.id, reverse=True)
        return items


class TicketInspectorRequestHandler(BaseHTTPRequestHandler):
    store = SightingStore()

    def do_POST(self) -> None:  # noqa: N802 - required by BaseHTTPRequestHandler
        path = urlparse(self.path).path
        if path != "/sightings":
            self._write_json(HTTPStatus.NOT_FOUND, {"error": "Not found"})
            return

        try:
            body = self._read_json_body()
            sighting = self.store.add(body)
        except ValueError as exc:
            self._write_json(HTTPStatus.BAD_REQUEST, {"error": str(exc)})
            return

        self._write_json(HTTPStatus.CREATED, asdict(sighting))

    def do_GET(self) -> None:  # noqa: N802 - required by BaseHTTPRequestHandler
        parsed = urlparse(self.path)
        if parsed.path != "/sightings":
            self._write_json(HTTPStatus.NOT_FOUND, {"error": "Not found"})
            return

        query = parse_qs(parsed.query)
        line = query.get("line", [None])[0]
        sightings = [asdict(item) for item in self.store.list(line=line)]
        self._write_json(HTTPStatus.OK, {"sightings": sightings})

    def _read_json_body(self) -> dict[str, Any]:
        length_header = self.headers.get("Content-Length")
        if not length_header:
            raise ValueError("Content-Length header is required")

        try:
            length = int(length_header)
        except ValueError as exc:  # pragma: no cover
            raise ValueError("Content-Length must be an integer") from exc

        raw = self.rfile.read(length)
        try:
            parsed = json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError("Request body must be valid JSON") from exc

        if not isinstance(parsed, dict):
            raise ValueError("Request body must be a JSON object")

        return parsed

    def _write_json(self, status: HTTPStatus, payload: dict[str, Any]) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: Any) -> None:  # noqa: A003
        return


def run_server(host: str = "127.0.0.1", port: int = 8080) -> None:
    server = ThreadingHTTPServer((host, port), TicketInspectorRequestHandler)
    server.serve_forever()
