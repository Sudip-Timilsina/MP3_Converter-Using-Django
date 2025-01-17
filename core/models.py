from django.db import models
from django.contrib.auth.models import User

class DownloadHistory(models.Model):
    title = models.CharField(max_length=255)
    audio_url = models.URLField()
    download_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Optional, track user who downloaded
    # Optionally add more fields, like the video ID or additional metadata

    def __str__(self):
        return f"{self.title} - {self.download_date}"
