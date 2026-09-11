from decimal import Decimal, ROUND_HALF_UP

from rest_framework import serializers


class EvaluationResponseSerializer(serializers.Serializer):
    decision_id = serializers.IntegerField()
    total_weight = serializers.DecimalField(max_digits=6, decimal_places=4)
    winner_option_id = serializers.IntegerField(allow_null=True)
    is_tie = serializers.BooleanField()
    rankings = serializers.ListField()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        for ranking in data["rankings"]:
            ranking["final_score"] = str(
                Decimal(str(ranking["final_score"])).quantize(
                    Decimal("0.01"),
                    rounding=ROUND_HALF_UP,
                )
            )
            for contribution in ranking["contributions"]:
                contribution["weight"] = str(contribution["weight"])
                contribution["score"] = str(contribution["score"])
                contribution["contribution"] = str(
                    Decimal(str(contribution["contribution"])).quantize(
                        Decimal("0.01"),
                        rounding=ROUND_HALF_UP,
                    )
                )
        return data