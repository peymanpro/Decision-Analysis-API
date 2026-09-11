from decimal import Decimal

from rest_framework import serializers

from .models import Score


class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = ("id", "option", "criterion", "score", "created_at", "updated_at")
        read_only_fields = ("id", "option", "criterion", "created_at", "updated_at")

    def validate_score(self, value):
        if value < Decimal("0") or value > Decimal("10"):
            raise serializers.ValidationError("Score must satisfy 0 <= score <= 10.")
        return value