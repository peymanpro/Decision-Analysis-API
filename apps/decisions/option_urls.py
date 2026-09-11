from django.urls import path

from .option_views import OptionDetailView, OptionListCreateView

urlpatterns = [
    path(
        "decisions/<int:decision_id>/options/",
        OptionListCreateView.as_view(),
        name="option-list-create",
    ),
    path(
        "options/<int:pk>/",
        OptionDetailView.as_view(),
        name="option-detail",
    ),
]
