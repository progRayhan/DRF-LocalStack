from django.db import models

class Document(models.Model):
    # Upload ANY file type to S3
    file = models.FileField(upload_to="documents/%Y/%m/%d/")

    # Optional metadata
    original_name = models.CharField(max_length=255)
    file_size = models.BigIntegerField()
    content_type = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Populate metadata automatically
        if self.file:
            self.original_name = self.file.name
            self.file_size = self.file.size
            self.content_type = getattr(self.file.file, "content_type", "")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.original_name
