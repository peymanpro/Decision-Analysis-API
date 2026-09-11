from django.urls import path

from .criteria_views import CriterionDetailView, CriterionListCreateView

urlpatterns = [
    path(
        "decisions/<int:decision_id>/criteria/",
        CriterionListCreateView.as_view(),
        name="criterion-list-create",
    ),
    path(
        "criteria/<int:pk>/",
        CriterionDetailView.as_view(),
        name="criterion-detail",
    ),
]
