from rest_framework import serializers

from .models import Token


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ("id", "user_hash", "token")
