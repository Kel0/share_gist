import json
from datetime import datetime
from http import HTTPStatus

from django.forms.models import model_to_dict
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from rest_framework.views import APIView

from share.utils import ApiResponse, token_verify  # noqa

from .models import Lexer, Paste
from .serializers import LexerSerializer, PasteSerializer


class LexersView(APIView):
    def __init__(self):
        super().__init__()
        self.lexer_model = Lexer()

    @token_verify
    def get(self, request):
        serializer = LexerSerializer(self.lexer_model.get_lexers_as_list(), many=True)
        return ApiResponse(
            status=HTTPStatus.OK,
            details=serializer.data,
        ).json

    @token_verify
    def post(self, request):
        lexer_name = json.loads(request.body.decode("utf-8")).get("lexer_name")

        if lexer_name is None:
            return ApiResponse(
                status=HTTPStatus.BAD_REQUEST, details="Invalid lexer_name variable."
            ).json

        lexer = self.lexer_model.create_lexer(name=lexer_name)
        if lexer is not None:
            serializer = LexerSerializer(lexer)
            return ApiResponse(status=HTTPStatus.CREATED, details=serializer.data).json

        return ApiResponse(
            status=HTTPStatus.BAD_REQUEST, details="Something went wrong."
        ).json


class PastesView(APIView):
    def __init__(self):
        super().__init__()
        self.paste_model = Paste()
        self.formatter = HtmlFormatter(lineanchors=True)

    @token_verify
    def get(self, request):
        uuid = request.GET.get("uuid")
        paste = self.paste_model.get_paste_by_uuid_as_list(unique_id=uuid)

        if len(paste) == 0:
            return ApiResponse(
                status=HTTPStatus.OK,
                details={},
            ).json

        serializer = PasteSerializer(paste[0])  # Тут все работает.
        html_code = highlight(
            serializer.data["content"],
            get_lexer_by_name(serializer.data["lexer"]["name"]),
            self.formatter,
        )
        paste = dict(serializer.data)
        paste["content"] = html_code

        return ApiResponse(
            status=HTTPStatus.OK,
            details=paste,
        ).json

    @token_verify
    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))
        lexer_id = data["lexer_id"]
        name = data["name"]
        content = data["code"]
        unix = data.get("inspiration_date")
        inspiration_date = 0 if not unix else datetime.fromtimestamp(int(unix))

        paste = self.paste_model.create_paste(
            lex_id=lexer_id,
            name=name,
            content=content,
            inspiration_date=inspiration_date,
        )
        if paste:
            _paste = model_to_dict(paste)
            _paste["lex"] = model_to_dict(paste.lex)

            return ApiResponse(status=HTTPStatus.CREATED, details=_paste).json

        return ApiResponse(
            status=HTTPStatus.BAD_REQUEST, details="Something went wrong."
        ).json
