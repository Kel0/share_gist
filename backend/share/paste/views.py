import json
from datetime import datetime
from http import HTTPStatus

from django.conf import settings
from django.core import serializers
from django.forms.models import model_to_dict
from django.http import HttpResponseForbidden, JsonResponse
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from rest_framework.views import APIView

from .models import Lexer, Paste


def token_verify(func):
    """
    Check the provided api_token
    :param func: Wrapped function
    :return: Function wrapper
    """

    def wrapper(obj, request):
        """
        Check api_token for all types of requests
        :param obj: APIView instance
        :param request: Django request
        :return: Function call or HttpResponseForbidden
        """
        request_types = ["GET", "POST", "HEAD", "DELETE", "PATCH", "PUT"]

        for request_type in request_types:
            if hasattr(request, request_type) is not None:
                if (
                    getattr(request, request_type).get("api_token")
                    == settings.API_TOKEN
                ):
                    return func(obj, request)
                return HttpResponseForbidden()

    return wrapper


class LexersView(APIView):
    """
    get:
    Return a list of all lexers.

    post:
    Create a new lexer instance.
    """

    def __init__(self):
        super().__init__()
        self.lexer_model = Lexer()

    @token_verify
    def get(self, request):
        """
        GET METHOD
        """
        lexers = serializers.serialize("json", self.lexer_model.get_lexers_as_list())
        return JsonResponse({"status": HTTPStatus.OK, "detail": json.loads(lexers)})

    @token_verify
    def post(self, request):
        lexer_name = json.loads(request.body.decode("utf-8")).get("lexer_name")

        if lexer_name is None:
            return JsonResponse(
                {
                    "type": HTTPStatus.BAD_REQUEST,
                    "detail": "Invalid lexer_name variable.",
                }
            )

        lexer = self.lexer_model.create_lexer(name=lexer_name)
        if lexer is not None:
            _lexer = model_to_dict(lexer)
            return JsonResponse({"status": HTTPStatus.CREATED, "details": _lexer})

        return JsonResponse(
            {"type": HTTPStatus.BAD_REQUEST, "details": "Something went wrong."}
        )


class PastesView(APIView):
    def __init__(self):
        super().__init__()
        self.paste_model = Paste()
        self.formatter = HtmlFormatter(lineanchors=True)

    @token_verify
    def get(self, request):
        uuid = request.GET.get("uuid")
        paste = self.paste_model.get_paste_by_uuid_as_list(unique_id=uuid)

        if len(paste) > 0:
            lexer_meta = model_to_dict(paste[0].lex)
            paste = model_to_dict(paste[0])
            paste["lex"] = lexer_meta
            paste["content"] = highlight(
                paste["content"],
                get_lexer_by_name(paste["lex"]["name"]),
                self.formatter,
            )

        else:
            paste = {}

        return JsonResponse({"status": HTTPStatus.OK, "details": paste})

    @token_verify
    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))
        lexer_id = data["lexer_id"]
        content = data["code"]
        unix = data.get("inspiration_date")
        inspiration_date = 0 if not unix else datetime.fromtimestamp(int(unix))
        print(inspiration_date)

        paste = self.paste_model.create_paste(
            lex_id=lexer_id, content=content, inspiration_date=inspiration_date
        )

        if paste:
            return JsonResponse(
                {"status": HTTPStatus.CREATED, "details": model_to_dict(paste)}
            )

        return JsonResponse(
            {"status": HTTPStatus.BAD_REQUEST, "details": "Something went wrong."}
        )
