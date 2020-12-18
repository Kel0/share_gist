from dataclasses import dataclass
from http import HTTPStatus
from typing import Dict, List, Union

from api_tokens.models import Token  # noqa
from django.conf import settings
from django.http import JsonResponse


@dataclass
class APIResponse:
    status: int
    details: Union[List, Dict, str] = "No details."

    @property
    def json(self):
        return JsonResponse(
            {"status": self.status, "details": self.details},
            status=self.status,
            safe=False,
        )


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    ip = request.META.get("REMOTE_ADDR")

    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]

    return ip


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
        :return: Function call send JsonResponse with fail message
        """
        user_ip = get_client_ip(request=request)
        request_types = ["GET", "POST", "HEAD", "DELETE", "PATCH", "PUT"]
        fail_details = "Invalid api_token parameter."
        tokens: List[str] = Token.get_tokens_as_list()

        for request_type in request_types:
            if hasattr(request, request_type) is not None:
                current_api_token = getattr(request, request_type).get("api_token")

                if current_api_token == settings.API_TOKEN_HASHED:
                    if user_ip in settings.ALLOWED_HOSTS_FOR_BASE_TOKEN_API:
                        return func(obj, request)

                elif current_api_token in tokens:
                    return func(obj, request)

                return APIResponse(
                    status=HTTPStatus.BAD_REQUEST,
                    details=fail_details,
                ).json

    return wrapper
