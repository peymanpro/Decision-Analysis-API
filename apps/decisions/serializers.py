from decimal import Decimal

from rest_framework import serializers

from .models import Criterion, Decision


class DecisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Decision
        fields = ("id", "title", "description", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")


class CriterionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Criterion
        fields = ("id", "name", "weight", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")

    def validate(self, attrs):
        decision = self.context.get("decision")
        name = attrs.get("name")

        if decision and name and Criterion.objects.filter(
            decision=decision,
            name=name,
        ).exists():
            raise serializers.ValidationError(
                {"name": "A criterion with this name already exists for this decision."}
            )

        return attrs

    def validate_weight(self, value):
        if value <= Decimal("0") or value > Decimal("1"):
            raise serializers.ValidationError("Weight must satisfy 0 < weight <= 1.")
        return value
