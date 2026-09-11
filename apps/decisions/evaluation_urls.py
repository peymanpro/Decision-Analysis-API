from django.urls import path

from .evaluation_views import DecisionEvaluationView

urlpatterns = [
    path(
        "decisions/<int:decision_id>/evaluate/",
        DecisionEvaluationView.as_view(),
        name="decision-evaluate",
    ),
]