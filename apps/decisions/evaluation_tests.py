from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase

from .evaluation_service import EvaluationError, EvaluationService
from .models import Criterion, Decision, Option, Score


User = get_user_model()


class EvaluationServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="evaluation-user",
            password="StrongPass123!",
        )
        self.decision = Decision.objects.create(
            owner=self.user,
            title="Laptop Decision",
        )
        self.cost = Criterion.objects.create(
            decision=self.decision,
            name="Cost",
            weight=Decimal("0.6000"),
        )
        self.quality = Criterion.objects.create(
            decision=self.decision,
            name="Quality",
            weight=Decimal("0.4000"),
        )
        self.option_a = Option.objects.create(
            decision=self.decision,
            name="Option A",
        )
        self.option_b = Option.objects.create(
            decision=self.decision,
            name="Option B",
        )

    def add_score(self, option, criterion, value):
        Score.objects.create(
            option=option,
            criterion=criterion,
            score=Decimal(value),
        )

    def test_evaluates_and_ranks_options(self):
        self.add_score(self.option_a, self.cost, "8.00")
        self.add_score(self.option_a, self.quality, "9.00")
        self.add_score(self.option_b, self.cost, "9.00")
        self.add_score(self.option_b, self.quality, "7.00")

        result = EvaluationService().evaluate(self.decision)

        self.assertEqual(result["total_weight"], Decimal("1"))
        self.assertEqual(result["winner_option_id"], self.option_a.id)
        self.assertFalse(result["is_tie"])
        self.assertEqual(result["rankings"][0]["rank"], 1)
        self.assertEqual(result["rankings"][0]["option_id"], self.option_a.id)
        self.assertEqual(result["rankings"][0]["final_score"], Decimal("8.40"))
        self.assertEqual(result["rankings"][1]["rank"], 2)
        self.assertEqual(result["rankings"][1]["final_score"], Decimal("8.20"))

    def test_missing_score_is_rejected(self):
        self.add_score(self.option_a, self.cost, "8.00")
        self.add_score(self.option_a, self.quality, "9.00")
        self.add_score(self.option_b, self.cost, "9.00")

        with self.assertRaises(EvaluationError) as context:
            EvaluationService().evaluate(self.decision)

        self.assertEqual(context.exception.code, "INCOMPLETE_SCORES")

    def test_invalid_weight_total_is_rejected(self):
        self.quality.weight = Decimal("0.3000")
        self.quality.save(update_fields=["weight"])

        self.add_score(self.option_a, self.cost, "8.00")
        self.add_score(self.option_a, self.quality, "9.00")
        self.add_score(self.option_b, self.cost, "9.00")
        self.add_score(self.option_b, self.quality, "7.00")

        with self.assertRaises(EvaluationError) as context:
            EvaluationService().evaluate(self.decision)

        self.assertEqual(context.exception.code, "INVALID_WEIGHTS")

    def test_tie_has_no_winner(self):
        for option in (self.option_a, self.option_b):
            self.add_score(option, self.cost, "8.00")
            self.add_score(option, self.quality, "9.00")

        result = EvaluationService().evaluate(self.decision)

        self.assertTrue(result["is_tie"])
        self.assertIsNone(result["winner_option_id"])
        self.assertEqual(result["rankings"][0]["rank"], 1)
        self.assertEqual(result["rankings"][1]["rank"], 1)