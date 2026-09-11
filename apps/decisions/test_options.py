from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from .models import Decision, Option

User = get_user_model()


class OptionAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="option_user",
            password="StrongPass123!",
        )
        self.other_user = User.objects.create_user(
            username="option_other",
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

    def test_create_option_for_owned_decision(self):
        response = self.client.post(
            f"/api/v1/decisions/{self.decision.id}/options/",
            {"name": "Company A"},
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        option = Option.objects.get(pk=response.data["id"])
        self.assertEqual(option.decision, self.decision)

    def test_duplicate_option_name_is_rejected(self):
        Option.objects.create(
            decision=self.decision,
            name="Company A",
        )

        response = self.client.post(
            f"/api/v1/decisions/{self.decision.id}/options/",
            {"name": "Company A"},
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("name", response.data)

    def test_other_users_decision_is_not_accessible(self):
        response = self.client.post(
            f"/api/v1/decisions/{self.other_decision.id}/options/",
            {"name": "Company A"},
            format="json",
        )

        self.assertEqual(response.status_code, 404)

    def test_list_returns_only_owned_options(self):
        Option.objects.create(
            decision=self.decision,
            name="Company A",
        )
        Option.objects.create(
            decision=self.other_decision,
            name="Company B",
        )

        response = self.client.get("/api/v1/decisions/%s/options/" % self.decision.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Company A")

    def test_delete_owned_option(self):
        option = Option.objects.create(
            decision=self.decision,
            name="Company A",
        )

        response = self.client.delete(f"/api/v1/options/{option.id}/")

        self.assertEqual(response.status_code, 204)
        self.assertFalse(Option.objects.filter(pk=option.id).exists())
