from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from .models import Decision

User = get_user_model()


class DecisionAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="decision_user",
            password="StrongPass123!",
        )
        self.other_user = User.objects.create_user(
            username="other_user",
            password="StrongPass123!",
        )
        self.client.force_authenticate(self.user)

    def test_create_decision_assigns_current_user(self):
        response = self.client.post(
            "/api/v1/decisions/",
            {"title": "Choosing a Job", "description": "Compare offers"},
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        decision = Decision.objects.get(pk=response.data["id"])
        self.assertEqual(decision.owner, self.user)

    def test_list_returns_only_owned_decisions(self):
        Decision.objects.create(owner=self.user, title="My Decision")
        Decision.objects.create(owner=self.other_user, title="Other Decision")

        response = self.client.get("/api/v1/decisions/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "My Decision")

    def test_detail_of_other_users_decision_is_not_accessible(self):
        decision = Decision.objects.create(
            owner=self.other_user,
            title="Private Decision",
        )

        response = self.client.get(f"/api/v1/decisions/{decision.id}/")

        self.assertEqual(response.status_code, 404)

    def test_update_owned_decision(self):
        decision = Decision.objects.create(
            owner=self.user,
            title="Old Title",
        )

        response = self.client.patch(
            f"/api/v1/decisions/{decision.id}/",
            {"title": "New Title"},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        decision.refresh_from_db()
        self.assertEqual(decision.title, "New Title")

    def test_delete_owned_decision(self):
        decision = Decision.objects.create(
            owner=self.user,
            title="Delete Me",
        )

        response = self.client.delete(f"/api/v1/decisions/{decision.id}/")

        self.assertEqual(response.status_code, 204)
        self.assertFalse(Decision.objects.filter(pk=decision.id).exists())
