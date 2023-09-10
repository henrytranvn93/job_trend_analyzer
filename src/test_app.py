# test_app.py

import unittest
from app import app

class TestApp(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_echo_input(self):
        response = self.client.post("/echo_user_input", data={"user_input": "Alice"})
        self.assertIn(b"Hello Alice! Nice to meet you", response.data)

    def test_integration(self):
        # Access the main page
        response = self.client.get("/")
        self.assertIn(b"<form action=\"/echo_user_input\" method=\"POST\">", response.data)

        # Simulate submitting the form with a POST request
        response = self.client.post("/echo_user_input", data={"user_input": "Bob"})
        self.assertIn(b"Hello Bob! Nice to meet you", response.data)

