from django.db import models
from django.forms import ValidationError


class Classification(models.Model):
    name = models.CharField(max_length=255, unique=True)
    level = models.IntegerField(unique=True)

    def __str__(self):
        return self.name


class AccessAttribute(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class DataTable(models.Model):
    name = models.CharField(max_length=100, unique=True)
    classification = models.ForeignKey(Classification, on_delete=models.PROTECT)
    access_attributes = models.ManyToManyField(AccessAttribute, blank=True)

    def __str__(self):
        return self.name


class DataRow(models.Model):
    table = models.ForeignKey(DataTable, on_delete=models.CASCADE)
    classification = models.ForeignKey(Classification, on_delete=models.PROTECT, blank=True, null=True)
    access_attributes = models.ManyToManyField(AccessAttribute, blank=True)

    def __str__(self):
        return f"({self.id}) Row in {self.table}"


class DataColumn(models.Model):
    table = models.ForeignKey(DataTable, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    classification = models.ForeignKey(Classification, on_delete=models.PROTECT, blank=True, null=True)
    access_attributes = models.ManyToManyField(AccessAttribute, blank=True)

    class Meta:
        unique_together = ("table", "name")

    def __str__(self):
        return f"{self.name} in {self.table}"


class DataCell(models.Model):
    row = models.ForeignKey(DataRow, on_delete=models.CASCADE)
    column = models.ForeignKey(DataColumn, on_delete=models.CASCADE)
    data = models.TextField()
    classification = models.ForeignKey(Classification, on_delete=models.PROTECT, blank=True, null=True)
    access_attributes = models.ManyToManyField(AccessAttribute, blank=True)

    class Meta:
        unique_together = ("row", "column")

    def clean(self):
        super().clean()

        if self.row.table != self.column.table:
            raise ValidationError("Row and column must belong to the same table.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Cell ({self.row}, {self.column})"
