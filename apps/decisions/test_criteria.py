from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from .models import Criterion, Decision

User = get_user_model()


class CriterionAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="criterion_user",
            password="StrongPass123!",
        )
        self.other_user = User.objects.create_user(
            username="criterion_other",
            password="StrongPass123!",
        )
        self.decision = Decision.objects.create(
            owner=self.user,
            title="Choosing a Job",
        )
        self.other_decision = Decision.objects.create(
            owner=self.other_user,
            title="Other Decision",
        )
        self.client.force_authenticate(self.user)

    def test_create_criterion_for_owned_decision(self):
        response = self.client.post(
            f"/api/v1/decisions/{self.decision.id}/criteria/",
            {"name": "Salary", "weight": "0.4000"},
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        criterion = Criterion.objects.get(pk=response.data["id"])
        self.assertEqual(criterion.decision, self.decision)

    def test_invalid_weight_is_rejected(self):
        response = self.client.post(
            f"/api/v1/decisions/{self.decision.id}/criteria/",
            {"name": "Salary", "weight": "0"},
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("weight", response.data)

    def test_weight_above_one_is_rejected(self):
        response = self.client.post(
            f"/api/v1/decisions/{self.decision.id}/criteria/",
            {"name": "Salary", "weight": "1.0001"},
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("weight", response.data)

    def test_other_users_decision_is_not_accessible(self):
        response = self.client.post(
            f"/api/v1/decisions/{self.other_decision.id}/criteria/",
            {"name": "Salary", "weight": "0.4000"},
            format="json",
        )

        self.assertEqual(response.status_code, 404)

    def test_duplicate_criterion_name_is_rejected(self):
        Criterion.objects.create(
            decision=self.decision,
            name="Salary",
            weight="0.4000",
        )

        response = self.client.post(
            f"/api/v1/decisions/{self.decision.id}/criteria/",
            {"name": "Salary", "weight": "0.3000"},
            format="json",
        )

        self.assertEqual(response.status_code, 400)
