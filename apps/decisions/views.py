from rest_framework import permissions, viewsets

from .models import Decision
from .serializers import DecisionSerializer


class DecisionViewSet(viewsets.ModelViewSet):
    serializer_class = DecisionSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Decision.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
