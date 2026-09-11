from decimal import Decimal

from django.conf import settings
from django.db import models


class Decision(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="decisions",
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.title


class Criterion(models.Model):
    decision = models.ForeignKey(
        Decision,
        on_delete=models.CASCADE,
        related_name="criteria",
    )
    name = models.CharField(max_length=200)
    weight = models.DecimalField(max_digits=6, decimal_places=4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("id",)
        constraints = [
            models.UniqueConstraint(
                fields=("decision", "name"),
                name="unique_criterion_name_per_decision",
            ),
            models.CheckConstraint(
                condition=models.Q(
                    weight__gt=Decimal("0"),
                    weight__lte=Decimal("1"),
                ),
                name="criterion_weight_between_zero_and_one",
            ),
        ]

    def __str__(self):
        return self.name


class Option(models.Model):
    decision = models.ForeignKey(
        Decision,
        on_delete=models.CASCADE,
        related_name="options",
    )
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("id",)
        constraints = [
            models.UniqueConstraint(
                fields=("decision", "name"),
                name="unique_option_name_per_decision",
            ),
        ]

    def __str__(self):
        return self.name


class Score(models.Model):
    option = models.ForeignKey(
        Option,
        on_delete=models.CASCADE,
        related_name="scores",
    )
    criterion = models.ForeignKey(
        Criterion,
        on_delete=models.CASCADE,
        related_name="scores",
    )
    score = models.DecimalField(max_digits=4, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("id",)
        constraints = [
            models.UniqueConstraint(
                fields=("option", "criterion"),
                name="unique_score_per_option_criterion",
            ),
            models.CheckConstraint(
                condition=models.Q(score__gte=Decimal("0"), score__lte=Decimal("10")),
                name="score_between_zero_and_ten",
            ),
        ]

    def __str__(self):
        return f"{self.option} - {self.criterion}: {self.score}"
