from django.db import models
from django.contrib.auth.models import User

class File(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="files")
    file = models.FileField(upload_to='')  # Stores the uploaded file locally
    uploaded_at = models.DateTimeField(auto_now_add=True)
    document_type = models.CharField(max_length=100, blank=True, null=True, default="Unknown")
    summary = models.TextField(blank=True, null=True, default="Failed to process")
    additional_info = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.file.name

class KeyEntity(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE, related_name="key_entities")
    name = models.CharField(max_length=255)
    value = models.TextField(blank=True, null=True)
    entity_type = models.CharField(max_length=100, blank=True, null=True)  # Optional: "Person", "Place", etc.

    def __str__(self):
        return f"{self.name}: {self.value or 'N/A'}"
