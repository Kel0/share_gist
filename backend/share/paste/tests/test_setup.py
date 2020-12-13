from django.conf import settings
from django.urls import reverse
from rest_framework.test import APITestCase


class APITestSetup(APITestCase):
    def setUp(self) -> None:
        self.api_token = settings.API_TOKEN_HASHED
        self.lexers_url = reverse("lexers") + "?api_token={token}".format(
            token=settings.API_TOKEN_HASHED
        )
        self.pastes_url = reverse("snippet") + "?api_token={token}".format(
            token=settings.API_TOKEN_HASHED
        )

        self.example_lexer = {"lexer_name": "Python"}
        self.example_paste = {
            "lexer_id": 1,
            "name": "Snippet",
            "code": "print('Hello, world!')",
        }

        return super().setUp()

    def _setup_lexer(self) -> dict:
        lexer = self.client.post(
            self.lexers_url, data=self.example_lexer, format="json"
        )
        return lexer.json()

    def _setup_paste(self) -> dict:
        paste = self.client.post(
            self.pastes_url, data=self.example_paste, format="json"
        )
        return paste.json()

    def tearDown(self) -> None:
        return super().tearDown()
