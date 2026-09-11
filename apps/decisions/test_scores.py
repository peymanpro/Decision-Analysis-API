from decimal import Decimal

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Criterion, Decision, Option, Score

User = get_user_model()

class ScoreApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="score-user", password="StrongPass123!")
        self.other_user = User.objects.create_user(username="other-user", password="StrongPass123!")
        self.client.force_authenticate(self.user)
        self.decision = Decision.objects.create(owner=self.user, title="Test Decision")
        self.criterion = Criterion.objects.create(
            decision=self.decision,
            name="Cost",
            weight=Decimal("0.5000"),
        )
        self.option = Option.objects.create(decision=self.decision, name="Option A")
        self.url = f"/api/v1/options/{self.option.id}/scores/{self.criterion.id}/"

    def test_create_score(self):
        response = self.client.put(self.url, {"score": "8.50"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["score"], "8.50")
        self.assertEqual(Score.objects.count(), 1)

    def test_update_existing_score(self):
        Score.objects.create(option=self.option, criterion=self.criterion, score=Decimal("7.00"))
        response = self.client.put(self.url, {"score": "9.25"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["score"], "9.25")
        self.assertEqual(Score.objects.count(), 1)

    def test_score_above_ten_is_rejected(self):
        response = self.client.put(self.url, {"score": "10.01"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Score.objects.count(), 0)

    def test_score_with_more_than_two_decimals_is_rejected(self):
        response = self.client.put(self.url, {"score": "8.123"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Score.objects.count(), 0)

    def test_other_users_option_is_not_accessible(self):
        other_decision = Decision.objects.create(owner=self.other_user, title="Other Decision")
        other_criterion = Criterion.objects.create(
            decision=other_decision,
            name="Cost",
            weight=Decimal("1.0000"),
        )
        other_option = Option.objects.create(decision=other_decision, name="Other Option")
        response = self.client.put(
            f"/api/v1/options/{other_option.id}/scores/{other_criterion.id}/",
            {"score": "8.00"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Score.objects.count(), 0)
