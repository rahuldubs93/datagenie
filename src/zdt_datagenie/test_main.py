import unittest
from fastapi.testclient import TestClient

from main import app


class ApiTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_main(self):
        response = self.client.get("/datagenie/v0")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(), {"Application": "Data Genie", "Environment": "dev"}
        )
