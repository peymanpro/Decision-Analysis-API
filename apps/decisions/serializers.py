from rest_framework import serializers

from .models import Decision


class DecisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Decision
        fields = ("id", "title", "description", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")
