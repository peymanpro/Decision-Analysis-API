from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Criterion, Option, Score
from .score_serializers import ScoreSerializer

class ScoreUpsertView(APIView):
    serializer_class = ScoreSerializer
    permission_classes = (IsAuthenticated,)

    def put(self, request, option_id, criterion_id):
        option = get_object_or_404(
            Option.objects.select_related("decision"),
            pk=option_id,
            decision__owner=request.user,
        )
        criterion = get_object_or_404(
            Criterion.objects.select_related("decision"),
            pk=criterion_id,
            decision=option.decision,
        )

        serializer = ScoreSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        score, created = Score.objects.update_or_create(
            option=option,
            criterion=criterion,
            defaults={"score": serializer.validated_data["score"]},
        )

        output = ScoreSerializer(score)
        return Response(
            output.data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )
