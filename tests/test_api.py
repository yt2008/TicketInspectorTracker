import json
import threading
import time
import unittest
from http.client import HTTPConnection
from http.server import ThreadingHTTPServer

from ticket_inspector_tracker.api import SightingStore, TicketInspectorRequestHandler


class TicketInspectorAPITests(unittest.TestCase):
    def setUp(self) -> None:
        TicketInspectorRequestHandler.store = SightingStore()
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), TicketInspectorRequestHandler)
        self.port = self.server.server_address[1]
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        time.sleep(0.01)

    def tearDown(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=1)

    def request(self, method: str, path: str, payload: dict | None = None):
        conn = HTTPConnection("127.0.0.1", self.port, timeout=2)
        headers = {}
        body = None
        if payload is not None:
            body = json.dumps(payload)
            headers["Content-Type"] = "application/json"
        conn.request(method, path, body=body, headers=headers)
        response = conn.getresponse()
        raw = response.read().decode("utf-8")
        parsed = json.loads(raw)
        conn.close()
        return response.status, parsed

    def test_report_and_retrieve_sighting(self) -> None:
        status, created = self.request(
            "POST",
            "/sightings",
            {"line": "U1", "stop": "Central Station", "direction": "North"},
        )
        self.assertEqual(status, 201)
        self.assertEqual(created["line"], "U1")
        self.assertEqual(created["stop"], "Central Station")
        self.assertEqual(created["inspector_count"], 1)

        status, listed = self.request("GET", "/sightings")
        self.assertEqual(status, 200)
        self.assertEqual(len(listed["sightings"]), 1)
        self.assertEqual(listed["sightings"][0]["id"], created["id"])

    def test_filter_sightings_by_line(self) -> None:
        self.request("POST", "/sightings", {"line": "U1", "stop": "A"})
        self.request("POST", "/sightings", {"line": "U2", "stop": "B"})

        status, listed = self.request("GET", "/sightings?line=U2")
        self.assertEqual(status, 200)
        self.assertEqual(len(listed["sightings"]), 1)
        self.assertEqual(listed["sightings"][0]["line"], "U2")

    def test_invalid_payload_is_rejected(self) -> None:
        status, error = self.request("POST", "/sightings", {"line": "", "stop": "A"})
        self.assertEqual(status, 400)
        self.assertIn("line is required", error["error"])


if __name__ == "__main__":
    unittest.main()
