from http import HTTPStatus

from .test_setup import APITestSetup


class TestLexer(APITestSetup):
    def test_post_lexer(self) -> None:
        response = self.client.post(
            self.lexers_url, data=self.example_lexer, format="json"
        )

        assert response.status_code == HTTPStatus.CREATED
        assert response.json() == {
            "status": 201,
            "details": {"id": 1, "name": "Python"},
        }

    def test_post_lexer_without_data(self) -> None:
        response = self.client.post(self.lexers_url, data={}, format="json")

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json() == {
            "status": 400,
            "details": "Invalid lexer_name variable.",
        }

    def test_update_lexer(self):
        lexer = self._setup_lexer()
        assert lexer["details"]["name"] == self.example_lexer["lexer_name"]

        response = self.client.put(
            self.lexers_url,
            data={"lexer_id": lexer["details"]["id"], "lexer_name": "Python2.7"},
            format="json",
        )
        assert response.json() == {
            "status": 200,
            "details": {"id": 1, "name": "Python2.7"},
        }

    def test_get_lexers(self) -> None:
        self.test_post_lexer()
        response = self.client.get(self.lexers_url)

        assert response.status_code == HTTPStatus.OK
        assert response.json() == {
            "status": 200,
            "details": [{"id": 1, "name": "Python"}],
        }

    def test_delete_lexer(self):
        self.test_get_lexers()
        response = self.client.delete(
            self.lexers_url, data={"lexer_id": 1}, format="json"
        )

        assert response.status_code == HTTPStatus.OK
        assert response.json() == {"status": 200, "details": True}


class TestPaste(APITestSetup):
    def test_post_paste(self) -> None:
        self._setup_lexer()
        response = self.client.post(
            self.pastes_url,
            data=self.example_paste,
            format="json",
        )

        assert response.status_code == HTTPStatus.CREATED

        json_response = response.json()
        json_response["details"]["uuid"] = "890dfc4e-3c68-11eb-99c7-a8a15909c179"
        json_response["details"]["inspiration_date"] = "2020-12-19T10:55:23.852"

        assert json_response == {
            "status": 201,
            "details": {
                "id": 1,
                "lex": {"id": 1, "name": "Python"},
                "name": "Snippet",
                "uuid": "890dfc4e-3c68-11eb-99c7-a8a15909c179",
                "content": (
                    '<div class="highlight"><pre><span></span><a name="True-1">'
                    '</a><span class="nb">print</span><span class="p">(</span><span'
                    ' class="s1">&#39;Hello, world!&#39;</span><span class="p">)'
                    "</span>\n</pre></div>\n"
                ),
                "inspiration_date": "2020-12-19T10:55:23.852",
            },
        }

    def test_update_paste(self) -> None:
        self._setup_lexer()
        paste = self._setup_paste()

        assert paste["details"]["name"] == self.example_paste["name"]
        assert paste["details"]["content"] == (
            '<div class="highlight"><pre><span></span><a name="True-1"></a><span '
            'class="nb">print</span><span class="p">(</span><span class="s1">&#39;Hello, '
            'world!&#39;</span><span class="p">)</span>\n</pre></div>\n'
        )

        response = self.client.put(
            self.pastes_url,
            data={
                "uuid": paste["details"]["uuid"],
                "name": "NewSnippet",
                "code": "print()",
            },
            format="json",
        )
        assert response.json()["details"]["name"] == "NewSnippet"
        assert response.json()["details"]["content"] == (
            '<div class="highlight"><pre><span></span><a name="True-1"></a>'
            '<span class="nb">print</span><span class="p">()</span>\n</pre></div>\n'
        )

    def test_delete_paste(self) -> None:
        self._setup_lexer()
        paste = self._setup_paste()

        response = self.client.delete(
            self.pastes_url, data={"uuid": paste["details"]["uuid"]}, format="json"
        )

        assert response.status_code == HTTPStatus.OK
        assert response.json() == {"status": 200, "details": True}

    def test_get_paste(self) -> None:
        self._setup_lexer()
        paste = self._setup_paste()

        response = self.client.get(
            self.pastes_url,
            {"api_token": self.api_token, "uuid": paste["details"]["uuid"]},
        )
        assert response.status_code == HTTPStatus.OK

        json_response = response.json()
        json_response["details"]["inspiration_date"] = "2020-12-19T10:55:23.852"

        assert json_response == {
            "status": 200,
            "details": {
                "id": 1,
                "lexer": {"id": 1, "name": "Python"},
                "name": "Snippet",
                "uuid": paste["details"]["uuid"],
                "content": (
                    '<div class="highlight"><pre><span></span><a name="True-1"></a>'
                    '<span class="nb">print</span><span class="p">(</span><span class='
                    '"s1">&#39;Hello, world!&#39;</span><span class="p">)</span>\n</pre></div>\n'
                ),
                "inspiration_date": "2020-12-19T10:55:23.852",
            },
        }
