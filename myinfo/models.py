from django.db import models
from django.contrib.sessions.models import Session

class OauthSessionState(models.Model):
    session = models.OneToOneField(Session, on_delete=models.CASCADE, primary_key=True)
    key = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
