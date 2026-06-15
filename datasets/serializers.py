from rest_framework import serializers
from .models import Dataset


class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = ['id', 'name', 'row_count', 'column_count', 'column_names', 'created_at']
        read_only_fields = ['id', 'row_count', 'column_count', 'column_names', 'created_at']


class DatasetUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = ['id', 'name', 'file', 'row_count', 'column_count', 'created_at']
        read_only_fields = ['id', 'row_count', 'column_count', 'created_at']

    def validate_file(self, value):
        if not value.name.lower().endswith('.csv'):
            raise serializers.ValidationError('Seuls les fichiers .csv sont acceptés.')
        if value.size > 50 * 1024 * 1024:
            raise serializers.ValidationError('Le fichier ne doit pas dépasser 50 Mo.')
        return value
