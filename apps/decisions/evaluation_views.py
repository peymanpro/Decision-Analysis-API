from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .evaluation_service import EvaluationError, EvaluationService
from .evaluation_serializers import EvaluationResponseSerializer
from .models import Decision


class DecisionEvaluationView(APIView):
    serializer_class = EvaluationResponseSerializer
    permission_classes = (IsAuthenticated,)

    def _evaluate(self, request, decision_id):
        decision = get_object_or_404(
            Decision,
            pk=decision_id,
            owner=request.user,
        )

        try:
            result = EvaluationService().evaluate(decision)
        except EvaluationError as exc:
            return Response(
                {"code": exc.code, "message": exc.message},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = EvaluationResponseSerializer(result)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, decision_id):
        return self._evaluate(request, decision_id)

    def get(self, request, decision_id):
        return self._evaluate(request, decision_id)