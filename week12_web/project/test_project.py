"""
test_project.py - automatic tests for your project. They make NO Claude calls:
they replace run_feature() with a fake, so they are fast, free and always give the same answer.

Run:  python project/test_project.py      (from the week12_web folder)
Your job: keep these passing as you change the starter, and write at least 2 tests of your own in MyTests.
"""

import logging
import os
import sys
import unittest
from pathlib import Path
from unittest import mock

from streamlit.testing.v1 import AppTest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(1, str(HERE.parent))
import feature      # noqa: E402
import flask_app    # noqa: E402
from llm import ClaudeCodeError   # noqa: E402

FAKE_RESULT = {"cards": [{"question": "What does 404 mean?", "answer": "Not Found."}]}
# Hide a harmless warning ("missing ScriptRunContext") that Streamlit prints when an app runs without a browser.
logging.getLogger("streamlit.runtime.scriptrunner_utils.script_run_context").addFilter(
    lambda record: "missing ScriptRunContext" not in record.getMessage())

TOKEN = "test-token-1234567890"        # a made-up token for the tests, not your real one


class FlaskTests(unittest.TestCase):
    def setUp(self):
        flask_app.app.testing = True
        self.client = flask_app.app.test_client()

    def test_health(self):
        self.assertEqual(self.client.get("/api/health").status_code, 200)

    def test_page_loads(self):
        self.assertEqual(self.client.get("/").status_code, 200)

    def test_empty_input_is_400(self):
        self.assertEqual(self.client.post("/api/run", json={}).status_code, 400)

    def test_too_long_is_400(self):
        r = self.client.post("/api/run", json={"text": "x" * (feature.MAX_CHARS + 1)})
        self.assertEqual(r.status_code, 400)

    def test_run_returns_result(self):
        with mock.patch.object(flask_app, "run_feature", return_value=FAKE_RESULT):
            r = self.client.post("/api/run", json={"text": "some notes"})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.get_json()["result"], FAKE_RESULT)

    def test_ai_down_is_503(self):
        with mock.patch.object(flask_app, "run_feature", side_effect=ClaudeCodeError("down")):
            r = self.client.post("/api/run", json={"text": "some notes"})
        self.assertEqual(r.status_code, 503)

    def test_stats_needs_the_token(self):
        with mock.patch.dict(os.environ, {"ADMIN_TOKEN": TOKEN}):
            self.assertEqual(self.client.get("/api/stats").status_code, 401)
            ok = self.client.get("/api/stats", headers={"X-Admin-Token": TOKEN})
        self.assertEqual(ok.status_code, 200)


class StreamlitTests(unittest.TestCase):
    def test_button_shows_the_result(self):
        at = AppTest.from_file(str(HERE / "streamlit_app.py"), default_timeout=30).run()
        with mock.patch.object(feature, "run_feature", return_value=FAKE_RESULT):
            at.text_area[0].input("some notes")
            at.button[0].click().run()
        self.assertFalse(at.exception)
        shown = " ".join(md.value for md in at.markdown)
        self.assertIn("What does 404 mean?", shown)


class MyTests(unittest.TestCase):
    """Write at least 2 tests for YOUR idea. Delete the skipTest lines when you write them.
    Ideas: format_result() on a result you write by hand; a 400 for an input your idea can't use;
    a new route you added; what the page shows when the AI is down."""

    def test_my_first_test(self):
        self.skipTest("TODO: write your first test")

    def test_my_second_test(self):
        self.skipTest("TODO: write your second test")


if __name__ == "__main__":
    unittest.main(verbosity=2)
