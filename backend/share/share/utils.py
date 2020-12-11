from dataclasses import dataclass
from http import HTTPStatus
from typing import Dict, List, Union

from django.conf import settings
from django.http import JsonResponse


@dataclass(frozen=True)
class PostTypes:
    CREATE: str = "create"
    EDIT: str = "edit"


@dataclass
class ApiResponse:
    status: int
    details: Union[List, Dict, str] = ""

    @property
    def json(self):
        return JsonResponse(
            {"status": self.status, "details": self.details},
            status=self.status,
            safe=False,
        )


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
        request_types = ["GET", "POST", "HEAD", "DELETE", "PATCH", "PUT"]

        for request_type in request_types:
            if hasattr(request, request_type) is not None:
                if (
                    getattr(request, request_type).get("api_token")
                    == settings.API_TOKEN_HASHED
                ):
                    return func(obj, request)
                return JsonResponse(
                    {
                        "status": HTTPStatus.BAD_REQUEST,
                        "details": "Invalid api_token parameter.",
                    }
                )

    return wrapper
