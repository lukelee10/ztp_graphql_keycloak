# Generated by Django 4.2.2 on 2023-06-26 21:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="AccessAttribute",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Classification",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255, unique=True)),
                ("level", models.IntegerField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="DataContent",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("text_data", models.TextField(blank=True, default=None, null=True)),
                ("bool_data", models.BooleanField(default=None, null=True)),
                ("image_data", models.ImageField(blank=True, null=True, upload_to="./media/images")),
                ("float_data", models.FloatField(blank=True, null=True)),
                ("email_data", models.EmailField(blank=True, max_length=254, null=True)),
                ("url_data", models.URLField(blank=True, null=True)),
                ("decimal_data", models.DecimalField(blank=True, decimal_places=10, max_digits=19, null=True)),
                ("int_data", models.IntegerField(blank=True, null=True)),
                ("date_data", models.DateField(blank=True, null=True)),
                ("dollar_data", models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="DataTable",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, unique=True)),
                ("access_attributes", models.ManyToManyField(blank=True, to="data_tables.accessattribute")),
                (
                    "classification",
                    models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="data_tables.classification"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="DataRow",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("access_attributes", models.ManyToManyField(blank=True, to="data_tables.accessattribute")),
                (
                    "classification",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="data_tables.classification",
                    ),
                ),
                (
                    "table",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="rows", to="data_tables.datatable"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="DataColumn",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100)),
                ("access_attributes", models.ManyToManyField(blank=True, to="data_tables.accessattribute")),
                (
                    "classification",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="data_tables.classification",
                    ),
                ),
                (
                    "table",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="columns", to="data_tables.datatable"
                    ),
                ),
            ],
            options={
                "unique_together": {("table", "name")},
            },
        ),
        migrations.CreateModel(
            name="DataCell",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("access_attributes", models.ManyToManyField(blank=True, to="data_tables.accessattribute")),
                (
                    "classification",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="data_tables.classification",
                    ),
                ),
                (
                    "column",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="cells", to="data_tables.datacolumn"
                    ),
                ),
                ("data", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="data_tables.datacontent")),
                (
                    "row",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="cells", to="data_tables.datarow"
                    ),
                ),
            ],
            options={
                "unique_together": {("row", "column")},
            },
        ),
    ]
