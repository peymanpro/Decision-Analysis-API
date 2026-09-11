from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions

from .models import Decision, Option
from .serializers import OptionSerializer


class OptionListCreateView(generics.ListCreateAPIView):
    serializer_class = OptionSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Option.objects.filter(decision__owner=self.request.user)

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


class OptionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OptionSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Option.objects.filter(decision__owner=self.request.user)
