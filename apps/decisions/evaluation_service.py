from decimal import Decimal

from .models import Decision, Score


class EvaluationError(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message
        super().__init__(message)


class EvaluationService:
    def evaluate(self, decision: Decision):
        criteria = list(decision.criteria.all().order_by("id"))
        options = list(decision.options.all().order_by("id"))

        if not criteria:
            raise EvaluationError(
                "NO_CRITERIA",
                "A decision must have at least one criterion.",
            )

        if not options:
            raise EvaluationError(
                "NO_OPTIONS",
                "A decision must have at least one option.",
            )

        total_weight = sum(
            (criterion.weight for criterion in criteria),
            Decimal("0"),
        )
        if total_weight != Decimal("1"):
            raise EvaluationError(
                "INVALID_WEIGHTS",
                "Criterion weights must sum exactly to 1.",
            )

        scores = {
            (score.option_id, score.criterion_id): score.score
            for score in Score.objects.filter(
                option__decision=decision,
                criterion__decision=decision,
            )
        }

        expected_score_count = len(options) * len(criteria)
        if len(scores) != expected_score_count:
            raise EvaluationError(
                "INCOMPLETE_SCORES",
                "Every option must have a score for every criterion.",
            )

        rankings = []

        for option in options:
            contributions = []
            final_score = Decimal("0")

            for criterion in criteria:
                score = scores[(option.id, criterion.id)]
                contribution = criterion.weight * score
                final_score += contribution
                contributions.append(
                    {
                        "criterion_id": criterion.id,
                        "criterion_name": criterion.name,
                        "weight": criterion.weight,
                        "score": score,
                        "contribution": contribution,
                    }
                )

            rankings.append(
                {
                    "option_id": option.id,
                    "option_name": option.name,
                    "final_score": final_score,
                    "contributions": contributions,
                }
            )

        rankings.sort(key=lambda item: item["final_score"], reverse=True)

        current_rank = 0
        previous_score = None

        for index, item in enumerate(rankings, start=1):
            if previous_score is None or item["final_score"] != previous_score:
                current_rank = index
            item["rank"] = current_rank
            previous_score = item["final_score"]

        top_score = rankings[0]["final_score"]
        top_items = [
            item for item in rankings
            if item["final_score"] == top_score
        ]

        is_tie = len(top_items) > 1
        winner_option_id = None if is_tie else top_items[0]["option_id"]

        return {
            "decision_id": decision.id,
            "total_weight": total_weight,
            "rankings": rankings,
            "winner_option_id": winner_option_id,
            "is_tie": is_tie,
        }