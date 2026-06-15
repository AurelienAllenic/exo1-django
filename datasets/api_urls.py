from django.urls import path
from .api_views import DatasetListCreateAPIView, DatasetRetrieveDestroyAPIView, dataset_analyze_api

urlpatterns = [
    path('datasets/', DatasetListCreateAPIView.as_view(), name='api-datasets'),
    path('datasets/<int:pk>/', DatasetRetrieveDestroyAPIView.as_view(), name='api-dataset-detail'),
    path('datasets/<int:pk>/analyze/', dataset_analyze_api, name='api-dataset-analyze'),
]
