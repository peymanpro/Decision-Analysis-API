from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions

from .models import Criterion, Decision
from .serializers import CriterionSerializer


class CriterionListCreateView(generics.ListCreateAPIView):
    serializer_class = CriterionSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Criterion.objects.filter(decision__owner=self.request.user)

    def get_decision(self):
        return get_object_or_404(
            Decision,
            pk=self.kwargs["decision_id"],
            owner=self.request.user,
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["decision"] = self.get_decision()
        return context

    def perform_create(self, serializer):
        serializer.save(decision=self.get_decision())


class CriterionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CriterionSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Criterion.objects.filter(decision__owner=self.request.user)
