import json
from datetime import datetime
from http import HTTPStatus

from django.forms.models import model_to_dict
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from rest_framework.views import APIView

from share.utils import APIResponse, token_verify  # noqa

from .models import Lexer, Paste
from .serializers import LexerSerializer, PasteSerializer
from .utils import convert_code_to_html


class LexersView(APIView):
    """
    Get/Update/Create/Delete lexer instances
    """

    def __init__(self):
        super().__init__()
        self.lexer_model = Lexer()

    @token_verify
    def get(self, request):
        """
        Get lexer instances
        """
        serializer = LexerSerializer(self.lexer_model.get_lexers_as_list(), many=True)
        return APIResponse(
            status=HTTPStatus.OK,
            details=serializer.data,
        ).json

    @token_verify
    def post(self, request):
        """
        Create lexer instance
        """
        lexer_name = json.loads(request.body.decode("utf-8")).get("lexer_name")

        if lexer_name is None:
            return APIResponse(
                status=HTTPStatus.BAD_REQUEST, details="Invalid lexer_name variable."
            ).json

        lexer = self.lexer_model.create_lexer(name=lexer_name)
        if lexer is not None:
            serializer = LexerSerializer(lexer)
            return APIResponse(status=HTTPStatus.CREATED, details=serializer.data).json

        return APIResponse(
            status=HTTPStatus.BAD_REQUEST, details="Something went wrong."
        ).json

    @token_verify
    def put(self, request):
        """
        Update lexer instance
        """
        data = json.loads(request.body.decode("utf-8"))
        lexer_id = data.get("lexer_id")
        lexer_name = data.get("lexer_name")

        if not lexer_name or not lexer_id:
            return APIResponse(
                status=HTTPStatus.BAD_REQUEST, details="Invalid parameters."
            ).json

        lexer = self.lexer_model.get_object_by_id(pk=lexer_id)
        if lexer is None:
            return APIResponse(
                status=HTTPStatus.NOT_FOUND,
                details="No lexer found under {lexer_id}".format(lexer_id=lexer_id),
            ).json

        lexer.name = lexer_name
        lexer.save()
        serializer = LexerSerializer(lexer)
        return APIResponse(status=HTTPStatus.OK, details=serializer.data).json

    @token_verify
    def delete(self, request):
        """
        Delete lexer instance
        """
        data = json.loads(request.body.decode("utf-8"))
        lexer = None
        lexer_id = data.get("lexer_id")
        lexer_name = data.get("lexer_name")

        if not lexer_id and not lexer_name:
            return APIResponse(
                status=HTTPStatus.BAD_REQUEST, details="Invalid parameters."
            ).json

        if lexer_id:
            lexer = self.lexer_model.get_object_by_id(pk=lexer_id)
        elif lexer_name:
            lexer = self.lexer_model.get_object_by_name(name=lexer_name)

        if lexer is None:
            return APIResponse(
                status=HTTPStatus.NOT_FOUND,
                details="No lexer under {lexer_id}".format(lexer_id=lexer_id),
            ).json

        lexer.delete()
        return APIResponse(status=HTTPStatus.OK, details=True).json


class PastesView(APIView):
    """
    Update/Create/Get/Delete paste instances
    """

    def __init__(self):
        super().__init__()
        self.paste_model = Paste()
        self.formatter = HtmlFormatter(lineanchors=True)

    @token_verify
    def get(self, request):
        """
        Get paste instances
        """
        uuid = request.GET.get("uuid")
        paste = self.paste_model.get_paste_by_uuid_as_list(unique_id=uuid)

        if len(paste) == 0:
            return APIResponse(
                status=HTTPStatus.NOT_FOUND,
                details="Paste not found.",
            ).json

        serializer = PasteSerializer(paste[0])
        paste = convert_code_to_html(serializer, self.formatter)

        return APIResponse(
            status=HTTPStatus.OK,
            details=paste,
        ).json

    @token_verify
    def post(self, request):
        """
        Create paste instance
        """
        data = json.loads(request.body.decode("utf-8"))
        lexer_id = data.get("lexer_id")
        name = data.get("name")
        content = data.get("code")
        unix = data.get("inspiration_date")
        inspiration_date = 0 if not unix else datetime.fromtimestamp(int(unix))

        if not lexer_id or not name or not content:
            return APIResponse(
                status=HTTPStatus.BAD_REQUEST, details="Invalid parameters."
            ).json

        paste = self.paste_model.create_paste(
            lex_id=lexer_id,
            name=name,
            content=content,
            inspiration_date=inspiration_date,
        )
        if paste:
            _paste = model_to_dict(paste)
            _paste["lex"] = model_to_dict(paste.lex)
            _paste["content"] = highlight(
                _paste["content"], get_lexer_by_name(paste.lex.name), self.formatter
            )

            return APIResponse(status=HTTPStatus.CREATED, details=_paste).json

        return APIResponse(
            status=HTTPStatus.BAD_REQUEST, details="Something went wrong."
        ).json

    @token_verify
    def put(self, request):
        """
        Update paste instance
        """
        data = json.loads(request.body.decode("utf-8"))
        uuid = data.get("uuid")
        name = data.get("name")
        content = data.get("code")

        if not uuid:
            return APIResponse(
                status=HTTPStatus.BAD_REQUEST, details="Invalid parameters."
            ).json

        paste = self.paste_model.get_paste_by_uuid_as_list(unique_id=uuid)

        if len(paste) == 0:
            return APIResponse(
                status=HTTPStatus.NOT_FOUND,
                details="No paste under {uuid}".format(uuid=uuid),
            ).json
        _paste = paste[0]

        if name:
            _paste.name = name
        if content:
            _paste.content = content

        _paste.save()
        serializer = PasteSerializer(_paste)
        return_paste = convert_code_to_html(serializer, self.formatter)

        return APIResponse(status=HTTPStatus.OK, details=return_paste).json

    @token_verify
    def delete(self, response):
        """
        Delete paste instance
        """
        data = json.loads(response.body.decode("utf-8"))
        uuid = data.get("uuid")

        if not uuid:
            return APIResponse(
                status=HTTPStatus.BAD_REQUEST, details="There is no uuid parameter."
            ).json

        paste = self.paste_model.get_object(unique_id=uuid)

        if paste is None:
            return APIResponse(
                status=HTTPStatus.NOT_FOUND,
                details="There is no paste under {uuid}.".format(uuid=uuid),
            ).json

        paste.delete()
        return APIResponse(status=HTTPStatus.OK, details=True).json
