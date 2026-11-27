import json
import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from core.api import app
from core.local_model import classify, parse_topic, LOCK

TOKEN = "a" * 64
BODY = {"question": "Como esta a margem?", "model": "qwen2.5:1.5b", "consent": True}
HEADERS = {"Origin": "http://localhost", "X-Lilium-Session": TOKEN}


def output(topic):
    return json.dumps({"done": True, "message": {"content": json.dumps({"topic": topic})}}).encode()


class LocalModelTests(unittest.TestCase):
    def test_parse_allowlist(self):
        self.assertEqual(parse_topic(output("insights")), "insights")
        for topic in ("unknown", "execute", "constructor", ["sales"]):
            self.assertIsNone(parse_topic(output(topic)))

    def test_reject_invalid_output(self):
        for raw in (b"bad", b"[]", b'{"done":false}', b'{"done":true,"message":{"content":"{}"}}'):
            self.assertIsNone(parse_topic(raw))

    def test_fixed_loopback_and_minimized_payload(self):
        with patch("core.local_model.http.client.HTTPConnection") as connection:
            conn = connection.return_value
            conn.getresponse.return_value.status = 200
            conn.getresponse.return_value.read.return_value = output("insights")
            self.assertEqual(classify(BODY["question"], BODY["model"]), "insights")
            connection.assert_called_once_with("127.0.0.1", 11434, timeout=20)
            args, kwargs = conn.request.call_args
            self.assertEqual(args, ("POST", "/api/chat"))
            sent = json.loads(kwargs["body"])
            self.assertEqual(sent["messages"][1], {"role": "user", "content": BODY["question"]})
            self.assertNotIn("tools", sent)
            self.assertFalse(sent["stream"])

    def test_reject_model_and_network_failure(self):
        with patch("core.local_model.http.client.HTTPConnection", side_effect=OSError) as connection:
            self.assertIsNone(classify("hi", "remote:cloud"))
            connection.assert_not_called()
            self.assertIsNone(classify("hi", BODY["model"]))

    def test_adversarial_output_rejected(self):
        for content in ('{"topic":"sales","topic":"finance"}', '{"topic":"sales","value":123}', '{"topic":NaN}', '["sales"]', 'sales'):
            raw = json.dumps({"done": True, "message": {"content": content}}).encode()
            self.assertIsNone(parse_topic(raw))
        self.assertIsNone(parse_topic(b'{"done":true,"done":true,"message":{}}'))
        self.assertIsNone(parse_topic(json.dumps({"done": True, "message": {"content": '{"topic":"sales"}', "tool_calls": [{"name": "anything"}]}}).encode()))
        self.assertIsNone(parse_topic(b"[" * 2000 + b"]" * 2000))

    def test_adversarial_request_rejected_before_model(self):
        client = TestClient(app, base_url="http://localhost")
        headers = {**HEADERS, "Content-Type": "application/json"}
        with patch.object(app.state, "session_token", TOKEN), patch("core.api.classify") as fn:
            for raw in (b'{"question":"hi","model":"qwen2.5:1.5b","consent":false,"consent":true}', b"[" * 1000 + b"]" * 1000, json.dumps({**BODY, "question": "x" + chr(0)}).encode(), json.dumps({**BODY, "question": chr(0xD800)}).encode()):
                self.assertEqual(client.post("/api/v1/copilot/route", content=raw, headers=headers).status_code, 422)
            self.assertEqual(client.post("/api/v1/copilot/route", content=b"x" * 2049, headers=headers).status_code, 413)
            fn.assert_not_called()

    def test_oversized_model_response(self):
        with patch("core.local_model.http.client.HTTPConnection") as connection:
            response = connection.return_value.getresponse.return_value
            response.status = 200
            response.read.return_value = b"x" * 16385
            self.assertIsNone(classify(BODY["question"], BODY["model"]))
            response.read.assert_called_once_with(16385)

    def test_busy(self):
        with LOCK:
            self.assertIsNone(classify("hi", BODY["model"]))

    def test_endpoint_requires_token_origin_and_consent(self):
        client = TestClient(app, base_url="http://localhost")
        with patch.object(app.state, "session_token", TOKEN), patch("core.api.classify", return_value="insights") as fn:
            self.assertEqual(client.post("/api/v1/copilot/route", json=BODY).status_code, 403)
            self.assertEqual(client.post("/api/v1/copilot/route", json=BODY, headers={"X-Lilium-Session": TOKEN}).status_code, 403)
            self.assertEqual(client.post("/api/v1/copilot/route", json={**BODY, "consent": False}, headers=HEADERS).status_code, 422)
            self.assertEqual(client.post("/api/v1/copilot/route", json={**BODY, "metrics": {}}, headers=HEADERS).status_code, 422)
            fn.assert_not_called()
            response = client.post("/api/v1/copilot/route", json=BODY, headers=HEADERS)
            self.assertEqual(response.json(), {"topic": "insights", "mode": "local-model-router"})
            fn.assert_called_once_with(BODY["question"], BODY["model"])

    def test_direct_development_disabled(self):
        with patch.object(app.state, "session_token", None):
            response = TestClient(app, base_url="http://localhost").post("/api/v1/copilot/route", json=BODY, headers=HEADERS)
            self.assertEqual(response.status_code, 403)
