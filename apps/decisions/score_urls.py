from django.urls import path

from .score_views import ScoreUpsertView

urlpatterns = [
    path(
        "options/<int:option_id>/scores/<int:criterion_id>/" ,
        ScoreUpsertView.as_view(),
        name="score-upsert",
    ),
]
