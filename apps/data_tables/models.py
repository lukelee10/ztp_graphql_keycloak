from enum import auto

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
    table = models.ForeignKey(DataTable, on_delete=models.CASCADE, related_name="rows")
    classification = models.ForeignKey(Classification, on_delete=models.PROTECT, blank=True, null=True)
    access_attributes = models.ManyToManyField(AccessAttribute, blank=True)

    def __str__(self):
        return f"({self.id}) Row in {self.table}"


class DataColumn(models.Model):
    table = models.ForeignKey(DataTable, on_delete=models.CASCADE, related_name="columns")
    name = models.CharField(max_length=100)
    classification = models.ForeignKey(Classification, on_delete=models.PROTECT, blank=True, null=True)
    access_attributes = models.ManyToManyField(AccessAttribute, blank=True)

    class Meta:
        unique_together = ("table", "name")

    def __str__(self):
        return f"{self.name} in {self.table}"


class DataContent(models.Model):
    text_data = models.TextField(blank=True, null=True, default=None)
    bool_data = models.BooleanField(null=True, default=None)
    image_data = models.ImageField(upload_to="./media/images", blank=True, null=True)
    float_data = models.FloatField(blank=True, null=True)
    email_data = models.EmailField(blank=True, null=True)
    url_data = models.URLField(blank=True, null=True)
    decimal_data = models.DecimalField(max_digits=19, decimal_places=10, blank=True, null=True)
    int_data = models.IntegerField(blank=True, null=True)
    date_data = models.DateField(blank=True, null=True)
    dollar_data = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    def __str__(self):
        if self.text_data:
            return self.text_data
        if self.bool_data is not None:
            return str(self.bool_data)
        if self.int_data:
            return str(self.int_data)
        if self.float_data:
            return self.float_data
        if self.email_data:
            return self.email_data
        if self.url_data:
            return str(self.url_data)
        if self.decimal_data:
            return self.decimal_data
        if self.image_data:
            return str(self.image_data.name)
        if self.date_data:
            return str(self.date_data)
        if self.dollar_data:
            return str(self.dollar_data)
        return super().__str__()


class DataCell(models.Model):
    row = models.ForeignKey(DataRow, on_delete=models.CASCADE, related_name="cells")
    column = models.ForeignKey(DataColumn, on_delete=models.CASCADE, related_name="cells")
    data = models.ForeignKey(DataContent, on_delete=models.CASCADE)
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
