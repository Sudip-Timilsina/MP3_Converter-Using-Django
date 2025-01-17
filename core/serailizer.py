from rest_framework import serializers
from .models import DownloadHistory

class DownloadHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DownloadHistory
        fields = ['title', 'audio_url', 'download_date', 'user']
