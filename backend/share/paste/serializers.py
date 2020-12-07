from rest_framework import serializers

from .models import Lexer, Paste


class LexerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lexer
        fields = ("id", "name")


class PasteSerializer(serializers.ModelSerializer):
    lexer = LexerSerializer(source="lex")

    class Meta:
        model = Paste
        fields = ("id", "lexer", "name", "uuid", "content", "inspiration_date")
