from __future__ import annotations

from hashlib import md5
from typing import List, Optional

from django.db import models


class Token(models.Model):
    user_hash = models.CharField(max_length=255)
    token = models.CharField(max_length=255, unique=True)

    @classmethod
    def get_object_by_token(cls, token: str) -> Optional[Token]:
        return cls.objects.get(token=token)  # noqa

    @classmethod
    def create_token(cls, name: str, token: str) -> Token:
        _token = cls(user_hash=md5(name).hexdigest(), token=token)
        _token.save()
        return _token

    @classmethod
    def get_tokens_as_list(cls) -> List[Token]:
        tokens = cls.objects.all()  # noqa
        return [obj.token for obj in tokens]
