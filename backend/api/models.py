from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class File(models.Model):
    user = models.ForeignObject(
        User, on_delete=models.CASCADE, related_name="files")
    file_name = models.CharField(max_length=255)
    file_url = models.URLField(max_length=255)
    file_size = models.PositiveIntegerField
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file_name
