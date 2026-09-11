from django.contrib import admin
from django.urls import include, path

from config.health import health

urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", health, name="health"),
    path("api/v1/auth/", include("apps.accounts.urls")),
    path("api/v1/", include("apps.decisions.urls")),
    path("api/v1/", include("apps.decisions.criteria_urls")),
    path("api/v1/", include("apps.decisions.option_urls")),
    path("api/v1/", include("apps.decisions.score_urls")),
]