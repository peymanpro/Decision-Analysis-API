from decimal import Decimal

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Criterion, Decision, Option, Score


User = get_user_model()


class EvaluationApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="evaluation-api-user",
            password="StrongPass123!",
        )
        self.other_user = User.objects.create_user(
            username="other-evaluation-user",
            password="StrongPass123!",
        )
        self.client.force_authenticate(self.user)
        self.decision = Decision.objects.create(
            owner=self.user,
            title="Evaluation API Decision",
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
        self.url = f"/api/v1/decisions/{self.decision.id}/evaluate/"

    def add_score(self, option, criterion, value):
        Score.objects.create(
            option=option,
            criterion=criterion,
            score=Decimal(value),
        )

    def populate_complete_scores(self):
        self.add_score(self.option_a, self.cost, "8.00")
        self.add_score(self.option_a, self.quality, "9.00")
        self.add_score(self.option_b, self.cost, "9.00")
        self.add_score(self.option_b, self.quality, "7.00")

    def test_post_evaluate_returns_result(self):
        self.populate_complete_scores()

        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["winner_option_id"], self.option_a.id)
        self.assertFalse(response.data["is_tie"])
        self.assertEqual(response.data["rankings"][0]["rank"], 1)

    def test_get_evaluate_returns_result(self):
        self.populate_complete_scores()

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["decision_id"], self.decision.id)
        self.assertEqual(response.data["rankings"][0]["final_score"], "8.40")

    def test_incomplete_scores_returns_400(self):
        self.add_score(self.option_a, self.cost, "8.00")

        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["code"], "INCOMPLETE_SCORES")

    def test_other_users_decision_returns_404(self):
        other_decision = Decision.objects.create(
            owner=self.other_user,
            title="Private Decision",
        )

        response = self.client.post(
            f"/api/v1/decisions/{other_decision.id}/evaluate/",
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)