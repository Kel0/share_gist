from __future__ import annotations

import uuid
from traceback import format_exc
from datetime import datetime, timedelta
from typing import List, Optional

from django.db import models


class Lexer(models.Model):
    name = models.CharField(max_length=225)

    @classmethod
    def get_lexers_as_list(cls) -> List[Lexer]:
        return list(cls.objects.all())  # noqa

    @classmethod
    def create_lexer(cls, name: str) -> Optional[Paste]:
        try:
            lexer = cls.objects.create(name=name)  # noqa
            return lexer

        except Exception as e_info:
            print(e_info)
            return None


class Paste(models.Model):
    lex = models.ForeignKey(Lexer, on_delete=models.CASCADE, null=False)
    uuid = models.CharField(max_length=255)
    content = models.TextField(default="")
    inspiration_date = models.DateField()

    @classmethod
    def get_paste_by_uuid_as_list(cls, unique_id: int):
        return cls.objects.all().filter(uuid=unique_id)  # noqa

    @classmethod
    def create_paste(
        cls, lex_id: int, content: str, inspiration_date: datetime
    ) -> Optional[Paste]:
        try:
            if inspiration_date == 0:
                paste = cls.objects.create(  # noqa
                    lex_id=lex_id,
                    content=content,
                    inspiration_date=datetime.now() + timedelta(days=7),
                    uuid=str(uuid.uuid1())
                )
                return paste

            paste = cls.objects.create(  # noqa
                lex_id=lex_id,
                content=content,
                uuid=str(uuid.uuid1()),
                inspiration_date=inspiration_date
            )
            return paste

        except Exception as e_info:
            print(format_exc())
            return None