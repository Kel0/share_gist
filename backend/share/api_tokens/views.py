import json
from http import HTTPStatus

from rest_framework.views import APIView

from share.utils import APIResponse, token_verify  # noqa

from .models import Token
from .serializers import TokenSerializer
from .utils import generate_token


class APITokens(APIView):  # Not active
    def __init__(self):
        super().__init__()
        self.tokens_model = Token()

    @token_verify
    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))

        if data["name"] is None:
            return APIResponse(
                status=HTTPStatus.BAD_REQUEST, detail="No required parameters provided."
            ).json

        token = self.tokens_model.create_token(
            name=data["name"], token=generate_token()
        )
        if token is None:
            return APIResponse(
                status=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Something went wrong."
            ).json

        serializer = TokenSerializer(token)

        return APIResponse(status=HTTPStatus.CREATED, detail=serializer.data).json
