from django.db import models


class Classification(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)


class Document(models.Model):
    title = models.CharField(max_length=255)
    classification = models.ForeignKey(Classification, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Portion(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="portions")
    classification = models.ForeignKey(Classification, on_delete=models.PROTECT)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
