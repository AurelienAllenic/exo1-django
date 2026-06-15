import json
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .models import Dataset
from .serializers import DatasetSerializer, DatasetUploadSerializer
from .utils import analyze_csv, NpEncoder


class DatasetListCreateAPIView(generics.ListCreateAPIView):
    """Liste tous les datasets de l'utilisateur connecté ou en crée un nouveau."""
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        return DatasetUploadSerializer if self.request.method == 'POST' else DatasetSerializer

    def get_queryset(self):
        return Dataset.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        dataset = serializer.save(user=self.request.user)
        try:
            analysis = analyze_csv(dataset.file.path)
            dataset.row_count = analysis['shape']['rows']
            dataset.column_count = analysis['shape']['cols']
            dataset.column_names = analysis['headers']
            dataset.save()
        except Exception:
            pass


class DatasetRetrieveDestroyAPIView(generics.RetrieveDestroyAPIView):
    """Récupère ou supprime un dataset spécifique."""
    serializer_class = DatasetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Dataset.objects.filter(user=self.request.user)


@extend_schema(
    description='Retourne l\'analyse complète d\'un dataset CSV : statistiques descriptives et données pour les graphiques.',
    responses={200: dict},
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dataset_analyze_api(request, pk):
    """Analyse complète d'un dataset (stats + données graphiques)."""
    try:
        dataset = Dataset.objects.get(pk=pk, user=request.user)
    except Dataset.DoesNotExist:
        return Response({'error': 'Dataset non trouvé.'}, status=status.HTTP_404_NOT_FOUND)

    try:
        analysis = analyze_csv(dataset.file.path)
        data = json.loads(json.dumps(analysis, cls=NpEncoder))
        return Response(data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
